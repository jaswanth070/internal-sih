from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Railway Controller", {"fields": ("role", "section")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "section", "is_staff")
    list_filter = ("role", "section", "is_staff", "is_superuser", "is_active")
