from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, SellerShop


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    """Define the admin pages for users."""
    model = User
    list_display = (
        "email", "first_name", "last_name", 'role', "is_active", "is_staff",)
    list_filter = ("email", "is_staff", "is_active", "role")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name",
                           "last_name", "username", "phone_number", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active",
                                    "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "first_name", "last_name", "is_staff",
                "username", "phone_number", "role",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telebotId', 'oblast', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'oblast', 'city')
    ordering = ('user', 'created_at')


@admin.register(SellerShop)
class SellerShopAdmin(admin.ModelAdmin):
    list_display = ('owner', 'shop_name', 'phone_number', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('owner', 'shop_name', 'phone_number')
    ordering = ('owner', 'created_at')
    prepopulated_fields = {'slug': ('shop_name',)}

