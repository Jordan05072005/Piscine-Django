from django.contrib import admin
from .models import User, Tip


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'reputation', 'is_staff', 'is_superuser')
    exclude = ('password',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(Tip)