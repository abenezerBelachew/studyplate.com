from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'identifier', 'full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('full_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Basic Information', {'fields': ('username', 'full_name', 'email', 'password', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Account Info', {'fields': ('date_joined', 'identifier',)}),
        
        # ('Follow system', {'fields': ('users_following', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'faculty', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('full_name', 'email',)
    ordering = ('full_name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)


