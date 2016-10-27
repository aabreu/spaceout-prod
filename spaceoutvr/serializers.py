from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

class SpaceoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'latitude', 'longitude', 'notification_id')
