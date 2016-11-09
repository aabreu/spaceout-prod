from django.db import models

from authemail.models import EmailUserManager, EmailAbstractUser
from spaceoutvr_django import settings

class SpaceoutUser(EmailAbstractUser):
    phone_number = models.CharField(max_length=30, default='')
    latitude = models.CharField(max_length=30, default='')
    longitude = models.CharField(max_length=30, default='')
    notification_id = models.CharField(max_length=256, default='')
    facebook_id = models.CharField(max_length=128, default='')
    reddit_id = models.CharField(max_length=128, default='')
    twitter_id = models.CharField(max_length=128, default='')
    soundcloud_id = models.CharField(max_length=128, default='')

    # Required
    objects = EmailUserManager()

class SpaceoutRoomDefinition(models.Model):
    ROOM_TYPE_HOME = 0
    ROOM_TYPE_360 = 1
    ROOM_TYPES = (
     (ROOM_TYPE_HOME, 'Home'),
     (ROOM_TYPE_360, '360 Theatre'),
    )

    type = models.IntegerField(default=0, choices=ROOM_TYPES)
    capacity = models.IntegerField(default=14)

    def __unicode__(self):
       return self.ROOM_TYPES[self.type][1]

class SpaceoutRoom(models.Model):
    user = models.ForeignKey(
        SpaceoutUser,
        on_delete = models.CASCADE,
    )

    definition = models.ForeignKey(
        SpaceoutRoomDefinition,
        on_delete = models.CASCADE,
        default = None,
    )

class SpaceoutContent(models.Model):
    CONTENT_TYPE_GIF = 0
    CONTENT_TYPE_IMAGE = 1
    CONTENT_TYPE_VIDEO = 2
    CONTENT_TYPES = (
     (CONTENT_TYPE_GIF, 'Gif'),
     (CONTENT_TYPE_IMAGE, 'Image'),
     (CONTENT_TYPE_VIDEO, 'Video'),
    )

    SOURCE_TYPE_GIPHY = 0
    SOURCE_TYPE_WIKI = 1
    SOURCE_TYPE_YOUTUBE = 2
    SOURCE_TYPE_GOOGLE_IMAGE = 3
    SOURCE_TYPES = (
     (SOURCE_TYPE_GIPHY, 'Giphy'),
     (SOURCE_TYPE_WIKI, 'Wiki'),
     (SOURCE_TYPE_YOUTUBE, 'Youtube'),
     (SOURCE_TYPE_GOOGLE_IMAGE, 'Google Images'),
    )

    type = models.IntegerField(default=0, choices=CONTENT_TYPES)
    idx = models.IntegerField(default=0)
    source = models.IntegerField(default=0, choices=SOURCE_TYPES)
    query = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    room = models.ForeignKey(
        SpaceoutRoom,
        on_delete = models.CASCADE,
    )

class SpaceoutComment(models.Model):
    url = models.CharField(max_length=256)
    author = models.ForeignKey(
        SpaceoutUser,
        on_delete = models.CASCADE,
    )
    content = models.ForeignKey(
        SpaceoutContent,
        on_delete = models.CASCADE,
    )
