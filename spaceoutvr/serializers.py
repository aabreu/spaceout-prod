from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent


class SpaceoutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceoutContent
        fields = ('id', 'type', 'url', 'source', 'query', 'idx')

class SpaceoutRoomSerializer(serializers.ModelSerializer):
    spaceoutcontent_set = SpaceoutContentSerializer(many=True)
    class Meta:
        model = SpaceoutRoom
        fields = ('id', 'type', 'capacity', 'spaceoutcontent_set')
        # depth = 2

class SpaceoutUserSerializer(serializers.Serializer):
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
