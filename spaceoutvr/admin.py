from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from spaceoutvr.models import *

class SpaceoutUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff',
        #                                'is_superuser', 'is_verified',
        #                                'groups', 'user_permissions')}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('SpaceoutVR', {'fields': ('phone_number', 'latitude', 'longitude', 'notification_id', 'facebook_id', 'twitter_id', 'soundcloud_id', 'reddit_id')}),
    )
    model = SpaceoutUser

class SpaceoutRoomAdmin(admin.ModelAdmin):
    list_display = ['user']

class SpaceoutRoomDefinitionAdmin(admin.ModelAdmin):
    list_display = ('type', 'capacity')

class SpaceoutContentAdmin(admin.ModelAdmin):
    list_display = ('idx','type','source','query','admin_image')

class SpaceoutCommentAdmin(admin.ModelAdmin):
    list_display = ('author','content')

class SpaceoutNotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'comment')

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), SpaceoutUserAdmin)
admin.site.register(SpaceoutRoom, SpaceoutRoomAdmin)
admin.site.register(SpaceoutRoomDefinition, SpaceoutRoomDefinitionAdmin)
admin.site.register(SpaceoutContent, SpaceoutContentAdmin)
admin.site.register(SpaceoutComment, SpaceoutCommentAdmin)
admin.site.register(SpaceoutNotification, SpaceoutNotificationAdmin)
