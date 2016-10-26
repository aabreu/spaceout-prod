from django.db import models
from django.db.models.signals import post_save
from authemail.models import EmailUserManager, EmailAbstractUser
from spaceoutvr_django import settings

class SpaceoutUser(EmailAbstractUser):
    # Required
    objects = EmailUserManager()

class SpaceoutProfile(models.Model):
    phone_number = models.CharField(max_length=30, default='')
    latitude = models.CharField(max_length=30, default='')
    longitude = models.CharField(max_length=30, default='')
    notification_id = models.CharField(max_length=256, default='')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_of',
    )

class SpaceoutRoom(models.Model):
    ROOM_TYPE_HOME = 0
    ROOM_TYPE_360 = 1
    ROOM_TYPES = (
     (ROOM_TYPE_HOME, 'Home'),
     (ROOM_TYPE_360, '360 Theatre'),
    )

    type = models.IntegerField(default=0, choices=ROOM_TYPES)
    user = models.ForeignKey(
        'SpaceoutUser',
        on_delete = models.CASCADE,
    )

class SpaceoutContent(models.Model):
    CONTENT_TYPE_IMAGE = 0
    CONTENT_TYPE_VIDEO = 1
    CONTENT_TYPES = (
     (CONTENT_TYPE_IMAGE, 'Image'),
     (CONTENT_TYPE_VIDEO, 'Video'),
    )

    SOURCE_TYPE_GIPHY = 0
    SOURCE_TYPE_WIKI = 1
    SOURCE_TYPE_YOUTUBE = 2
    SOURCE_TYPE_GOOGLE_IMAGE = 3
    SOURCE_TYPES = (
     (SOURCE_TYPE_GIPHY, 'Giphy'),
     (SOURCE_TYPE_WIKI, 'Video'),
     (SOURCE_TYPE_YOUTUBE, 'Youtube'),
     (SOURCE_TYPE_GOOGLE_IMAGE, 'Google Images'),
    )

    type = models.IntegerField(default=0, choices=CONTENT_TYPES)
    source = models.IntegerField(default=0, choices=SOURCE_TYPES)
    query = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    room = models.ForeignKey(
        'SpaceoutRoom',
        on_delete = models.CASCADE,
    )

def init_spaceout_user(**kwargs):
    print("SAVE HOOK")
    instance = kwargs.get('instance')
    is_new = kwargs.get('created')

    for key in kwargs:
        print key

    if is_new:
        print("SAVING PROFILE")
        profile = SpaceoutProfile(user=instance)
        profile.save()
        instance.profile = profile
        instance.save()

post_save.connect(init_spaceout_user, SpaceoutUser)
