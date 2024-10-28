from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from mdl.models import Recipe

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'blood_sugar_target', 'height', 'weight', 'is_staff']
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Personal info', {'fields': ('blood_sugar_target', 'height', 'weight')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('id',)
    ordering = ('id',)

admin.site.register(User, CustomUserAdmin)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
