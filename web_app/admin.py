from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    # Define the fields to be used in displaying the User model.
    list_display = ('username', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Fields for creating and editing the user (exclude non-existent fields)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Spotify Info', {'fields': ('access_token', 'refresh_token', 'time_obtained', 'expires_in')}),
    )

    # Add the fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)