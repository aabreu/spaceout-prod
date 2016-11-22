from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent, SpaceoutRoomDefinition, SpaceoutComment, SpaceoutNotification
from django.conf import settings

class SpaceoutUserSimpleSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = SpaceoutUser
        fields = ('id', 'email', 'first_name', 'last_name', 'latitude', 'longitude', 'notification_id',
                  'facebook_id', 'soundcloud_id', 'reddit_id', 'twitter_id')

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

class SpaceoutRoomDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceoutRoomDefinition
        fields = ('type', 'capacity')

class SpaceoutRoomSerializer(serializers.ModelSerializer):
    spaceoutcontent_set = SpaceoutContentSerializer(many=True)
    class Meta:
        model = SpaceoutRoom
        fields = ('id', 'definition', 'spaceoutcontent_set')
        depth = 2

class SpaceoutUserSerializer(serializers.ModelSerializer):
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
    personality_insights = serializers.CharField();
    spaceoutroom_set = SpaceoutRoomSerializer(many=True)
    class Meta:
        model = SpaceoutUser
        fields = ('id', 'first_name', 'last_name', 'latitude', 'longitude', 'personality_insights', 'notification_id',
                  'facebook_id', 'soundcloud_id', 'reddit_id', 'twitter_id', 'email',
                  'spaceoutroom_set')

    depth = 2

class SpaceoutNotificationSerializer(serializers.ModelSerializer):
    def get_content(self, notification):
        # return notification.comment.content.url
        return SpaceoutContentSerializer(notification.comment.content).data

    def get_comment_id(self, notification):
        return notification.comment.id

    def get_room_id(self, notification):
        return notification.comment.content.room.id

    def get_author(self, notification):
        return SpaceoutUserSimpleSerializer(notification.comment.author).data

    def get_members(self, notification):
        return SpaceoutUserSimpleSerializer(notification.comment.content.members(), many=True).data

    id = serializers.IntegerField()
    type = serializers.IntegerField()
    read = serializers.BooleanField()
    comment_id = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = SpaceoutNotification
        fields = ('id', 'type', 'read', 'comment_id', 'content',
                  'room_id', 'author', 'members')

class SpaceoutUserNotificationsSerializer(serializers.ModelSerializer):
    def get_new_count(self, user):
        return user.spaceoutnotification_set.filter(read=False).count()

    new_count = serializers.SerializerMethodField()
    spaceoutnotification_set = SpaceoutNotificationSerializer(many=True)


    class Meta:
        model = SpaceoutUser
        fields = ('new_count', 'spaceoutnotification_set')
