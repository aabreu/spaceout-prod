from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent, SpaceoutRoomDefinition, SpaceoutComment
from django.conf import settings

class SpaceoutUserSimpleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    facebook_id = serializers.CharField()
    soundcloud_id = serializers.CharField()
    reddit_id = serializers.CharField()
    twitter_id = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    notification_id = serializers.CharField()
    class Meta:
        model = SpaceoutUser
        fields = ('id', 'latitude', 'longitude', 'notification_id',
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
        fields = ('id', 'type', 'url', 'source', 'query', 'idx', 'spaceoutcomment_set')
        # depth = 2

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
    facebook_id = serializers.CharField()
    soundcloud_id = serializers.CharField()
    reddit_id = serializers.CharField()
    twitter_id = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    notification_id = serializers.CharField()
    spaceoutroom_set = SpaceoutRoomSerializer(many=True)
    class Meta:
        model = SpaceoutUser
        fields = ('id', 'latitude', 'longitude', 'notification_id',
                  'facebook_id', 'soundcloud_id', 'reddit_id', 'twitter_id',
                  'spaceoutroom_set')

    depth = 2
