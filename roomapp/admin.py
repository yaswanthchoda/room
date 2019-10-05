from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from roomapp.models import Profile, Room


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'occupation', 'birth_date')

    class Meta:
        model = Profile
        # fields = "__all__"

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_address')

    class Meta:
        model = Room
        # fields = "__all__"

admin.site.register(Profile,   ProfileAdmin)
admin.site.register(Room, RoomAdmin)