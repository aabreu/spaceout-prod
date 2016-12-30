from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent, SpaceoutRoomDefinition, SpaceoutComment, SpaceoutNotification
from spaceoutvr.models import WatsonBlacklist

from django.conf import settings

class SpaceoutUserSimpleSerializer(serializers.ModelSerializer):
    def get_personality_insights_output_url(self, user):
        return user.personality_insights_output_url.storage.url(user.personality_insights_output_url.name)

    def get_featured_input_url(self, user):
        return user.featured_input_url.storage.url(user.featured_input_url.name)

    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    facebook_id = serializers.CharField()
    soundcloud_id = serializers.CharField()
    reddit_id = serializers.CharField()
    twitter_id = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    notification_id = serializers.CharField()
    last_activity = serializers.DateTimeField()
    popularity = serializers.IntegerField()
    featured = serializers.BooleanField()
    personality_insights_output_url = serializers.SerializerMethodField()
    featured_input_url = serializers.SerializerMethodField()
    featured_page_url = serializers.CharField()
    avatar_url = serializers.CharField()

    class Meta:
        model = SpaceoutUser
        fields = ('id', 'email', 'first_name', 'last_name', 'featured', 'latitude', 'longitude', 'notification_id', 'last_activity', 'popularity',
                  'facebook_id', 'soundcloud_id', 'reddit_id', 'twitter_id', 'personality_insights_output_url', 'featured_input_url', 'featured_page_url', 'avatar_url')

    depth = 2


class SpaceoutCommentSerializer(serializers.ModelSerializer):
    def get_url(self, comment):
        return comment.audio_file.storage.url(comment.audio_file.name)

    def get_content_id(self, comment):
        return comment.content.id

    def get_room_id(self, comment):
        return comment.content.room.id

    author = SpaceoutUserSimpleSerializer()
    url = serializers.SerializerMethodField()
    content_id = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()
    class Meta:
        model = SpaceoutComment
        fields = ('id', 'url', 'author', 'content_id', 'room_id')
        # depth = 1

class SpaceoutContentSerializer(serializers.ModelSerializer):
    spaceoutcomment_set = SpaceoutCommentSerializer(many=True)
    class Meta:
        model = SpaceoutContent
        fields = ('id', 'type', 'url', 'source', 'query', 'weight', 'idx', 'spaceoutcomment_set')
        depth = 2

class SpaceoutContentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceoutContent
        fields = ('id', 'type', 'url', 'source', 'query', 'weight', 'idx')

class SpaceoutRoomDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceoutRoomDefinition
        fields = ('type', 'capacity')

class SpaceoutRoomSerializer(serializers.ModelSerializer):
    def get_owner(self, room):
        return SpaceoutUserSimpleSerializer(room.user).data

    spaceoutcontent_set = SpaceoutContentSerializer(many=True)
    owner = serializers.SerializerMethodField()
    class Meta:
        model = SpaceoutRoom
        fields = ('id', 'definition', 'spaceoutcontent_set', 'owner')
        depth = 2

class SpaceoutUserSerializer(serializers.ModelSerializer):
    def get_personality_insights_output_url(self, user):
        return user.personality_insights_output_url.storage.url(user.personality_insights_output_url.name)

    def get_featured_input_url(self, user):
        return user.featured_input_url.storage.url(user.featured_input_url.name)

    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_name = serializers.CharField()
    email = serializers.CharField()
    facebook_id = serializers.CharField()
    soundcloud_id = serializers.CharField()
    reddit_id = serializers.CharField()
    twitter_id = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    notification_id = serializers.CharField()
    featured = serializers.BooleanField()
    featured_page_url = serializers.CharField()
    featured_input_url = serializers.SerializerMethodField()
    avatar_url = serializers.CharField()
    personality_insights_output_url = serializers.SerializerMethodField()
    last_activity = serializers.DateTimeField()
    spaceoutroom_set = SpaceoutRoomSerializer(many=True)
    class Meta:
        model = SpaceoutUser
        fields = ('id', 'first_name', 'last_name', 'featured', 'latitude', 'longitude', 'notification_id',
                  'facebook_id', 'soundcloud_id', 'reddit_id', 'twitter_id', 'email',
                  'fb_gender', 'fb_location', 'fb_birthdate', 'featured_input_url', 'featured_page_url', 'avatar_url',
                  'personality_insights_output_url', 'last_activity',
                  'spaceoutroom_set')

    depth = 2

class SpaceoutNotificationSerializer(serializers.ModelSerializer):
    def get_content(self, notification):
        # return notification.comment.content.url
        return SpaceoutContentSimpleSerializer(notification.comment.content).data

    def get_comment_id(self, notification):
        return notification.comment.id

    def get_room_id(self, notification):
        return notification.comment.content.room.id

    def get_author(self, notification):
        return SpaceoutUserSimpleSerializer(notification.comment.author).data

    def get_members(self, notification):
        return SpaceoutUserSimpleSerializer(notification.comment.content.members(), many=True).data

    def get_owner(self, notification):
        return SpaceoutUserSimpleSerializer(notification.comment.content.room.user).data

    id = serializers.IntegerField()
    type = serializers.IntegerField()
    read = serializers.BooleanField()
    comment_id = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()

    content = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = SpaceoutNotification
        fields = ('id', 'type', 'read', 'comment_id', 'content',
                  'room_id', 'author', 'members', 'owner')

class SpaceoutUserNotificationsSerializer(serializers.ModelSerializer):
    def get_new_count(self, user):
        return user.spaceoutnotification_set.filter(read=False).count()

    new_count = serializers.SerializerMethodField()
    spaceoutnotification_set = SpaceoutNotificationSerializer(many=True)

    class Meta:
        model = SpaceoutUser
        fields = ('new_count', 'spaceoutnotification_set')

class WatsonBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatsonBlacklist
        fields = ('text',)

class PeopleSeriaizer(PaginationSerializer):
    class Meta:
        object_serializer_class = SpaceoutUserSimpleSerializer
