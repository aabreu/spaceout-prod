from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from spaceoutvr.models import *

class SpaceoutUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'signin_method')}),
        ('Personal Info', {'fields': ('user_name', 'first_name', 'last_name')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff',
        #                                'is_superuser', 'is_verified',
        #                                'groups', 'user_permissions')}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('SpaceoutVR', {'fields': ('featured', 'last_activity', 'phone_number', 'latitude', 'longitude', 'notification_id', 'facebook_id', 'twitter_id', 'soundcloud_id', 'reddit_id', 'fb_gender', 'fb_birthdate', 'fb_location', 'personality_insights_input_url', 'personality_insights_output_url', 'featured_input_url', 'featured_page_url', 'avatar_url')}),
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


class WatsonOutputAdmin(admin.ModelAdmin):
    list_display = ('text', 'relevance', 'analysis')


def unbound_callable(emp):
    return emp.car.rego

class WatsonOutputInline(admin.TabularInline):
    model = WatsonOutput
    fields = ('text', 'relevance', 'analysis')
    readonly_fields = ('text', 'relevance', 'analysis')

    def model_admin_callable(self, output):
        return output.text

class WatsonInputAdmin(admin.ModelAdmin):
    model = WatsonInput

    def temrs_count(self, instance):
        return instance.watsonoutput_set.all().count()

    list_display = ('user', 'recipe_id', 'social_network', 'chunk_id',  'temrs_count', 'data_size', 'watson_response_time', 'input_url')
    fields = ('user', 'recipe_id', 'social_network', 'chunk_id', 'data_size', 'watson_response_time', 'chunk_date_start', 'chunk_date_end', 'input_url')
    inlines = (WatsonOutputInline,)

class WatsonBlacklistAdmin(admin.ModelAdmin):
    model = WatsonBlacklist
    list_display = ('text',)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), SpaceoutUserAdmin)
admin.site.register(SpaceoutRoom, SpaceoutRoomAdmin)
admin.site.register(SpaceoutRoomDefinition, SpaceoutRoomDefinitionAdmin)
admin.site.register(SpaceoutContent, SpaceoutContentAdmin)
admin.site.register(SpaceoutComment, SpaceoutCommentAdmin)
admin.site.register(SpaceoutNotification, SpaceoutNotificationAdmin)
admin.site.register(WatsonInput, WatsonInputAdmin)
admin.site.register(WatsonOutput, WatsonOutputAdmin)
admin.site.register(WatsonBlacklist, WatsonBlacklistAdmin)
