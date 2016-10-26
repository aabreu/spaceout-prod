from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from spaceoutvr.models import *

class SpaceoutUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'is_verified',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class SpaceoutProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','latitude','longitude','notification_id']

class SpaceoutRoomAdmin(admin.ModelAdmin):
    list_display = ('type','user')

class SpaceoutContentAdmin(admin.ModelAdmin):
    list_display = ('type','source','query','url')


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), SpaceoutUserAdmin)
admin.site.register(SpaceoutProfile, SpaceoutProfileAdmin)
admin.site.register(SpaceoutRoom, SpaceoutRoomAdmin)
admin.site.register(SpaceoutContent, SpaceoutContentAdmin)
