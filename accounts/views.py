import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from rest_framework_simplejwt.tokens import RefreshToken

from .forms import LoginForm

def _generate_captcha(request: HttpRequest) -> str:
    a, b = random.randint(10, 99), random.randint(1, 9)
    answer = a + b
    request.session["captcha_answer"] = str(answer)
    return f"{a} + {b}"

def _verify_captcha(request: HttpRequest, user_value: str) -> bool:
    expected = request.session.get("captcha_answer")
    return expected is not None and expected == (user_value or "").strip()

@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = LoginForm()
        captcha_text = _generate_captcha(request)
        return render(request, "accounts/login.html", {"form": form, "captcha_text": captcha_text})

    # POST
    form = LoginForm(request.POST)
    captcha_text = _generate_captcha(request)  # regenerate for re-render on failure
    if not form.is_valid():
        return render(request, "accounts/login.html", {"form": form, "captcha_text": captcha_text}, status=400)

    if not _verify_captcha(request, form.cleaned_data["captcha"]):
        form.add_error("captcha", "Captcha does not match. Please try again.")
        return render(request, "accounts/login.html", {"form": form, "captcha_text": captcha_text}, status=400)

    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    user = authenticate(request, username=username, password=password)
    if user is None or not user.is_active:
        form.add_error(None, "Invalid credentials or inactive account.")
        return render(request, "accounts/login.html", {"form": form, "captcha_text": captcha_text}, status=401)

    # Log in the user for session-protected views (like the dashboard)
    login(request, user)

    # Create JWT tokens and set as HttpOnly cookies
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = redirect("accounts:dashboard")

    # Access token cookie (~1 hour)
    access_exp = timezone.now() + timedelta(minutes=60)
    response.set_cookie(
        "access",
        str(access),
        httponly=True,
        secure=False,  # set True when using HTTPS
        samesite="Lax",
        expires=access_exp,
        path="/",
    )
    # Refresh token cookie (~7 days)
    refresh_exp = timezone.now() + timedelta(days=7)
    response.set_cookie(
        "refresh",
        str(refresh),
        httponly=True,
        secure=False,  # set True when using HTTPS
        samesite="Lax",
        expires=refresh_exp,
        path="/",
    )

    messages.success(request, "Login successful.")
    return response

def dashboard_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    return render(request, "accounts/dashboard.html")

def logout_view(request: HttpRequest) -> HttpResponse:
    # Clear session and JWT cookies
    logout(request)
    response = redirect("accounts:login")
    response.delete_cookie("access", path="/")
    response.delete_cookie("refresh", path="/")
    messages.info(request, "Logged out.")
    return response
