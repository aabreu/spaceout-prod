from django.db import models

from authemail.models import EmailUserManager, EmailAbstractUser

from spaceoutvr_django import settings
from spaceoutvr.storage import CommentsStorage, WatsonStorage

import datetime

def comment_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.utcnow()
    name = now.strftime("%H_%M_%S_%f")
    return '{0}_{1}_{2}_{3}_{4}.wav'.format(
        now.year,
        now.month,
        now.day,
        instance.content.room.user.id,
        name,
    )

def watson_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.utcnow()
    name = now.strftime("%H_%M_%S_%f")
    return '{0}_{1}_{2}_{3}_{4}.txt'.format(
        now.year,
        now.month,
        now.day,
        instance.user.id,
        name,
    )

class SpaceoutUser(EmailAbstractUser):
    phone_number = models.CharField(max_length=30, default='')
    latitude = models.CharField(max_length=30, default='')
    longitude = models.CharField(max_length=30, default='')
    personality_insights = models.TextField(max_length=2048, null=True)
    notification_id = models.CharField(max_length=256, default='')
    facebook_id = models.CharField(max_length=128, default='')
    reddit_id = models.CharField(max_length=128, default='')
    twitter_id = models.CharField(max_length=128, default='')
    soundcloud_id = models.CharField(max_length=128, default='')
    fb_gender = models.CharField(max_length=10, default='')
    fb_location = models.CharField(max_length=128, default='')
    fb_birthdate = models.CharField(max_length=16, default='')

    # notifications = models.ManyToManyField('SpaceoutNotification')

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
    user = models.ForeignKey(SpaceoutUser, on_delete = models.CASCADE)

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
    weight = models.FloatField(default=0)
    url = models.CharField(max_length=2048)
    room = models.ForeignKey(SpaceoutRoom, on_delete = models.CASCADE)

    def admin_image(self):
        if self.type == self.CONTENT_TYPE_IMAGE:
            return '<img src="%s" width=\'100\' height=\'100\'/>' % self.url
        else:
            return '<video src="%s" width=\'100\' height=\'100\'/>' % self.url
    admin_image.allow_tags = True

    def members(self):
        result = set()
        for comment in self.spaceoutcomment_set.all():
            result.add(comment.author)
        return result

class SpaceoutComment(models.Model):
    url = models.CharField(max_length=256)
    audio_file = models.FileField(upload_to=comment_directory_path, default=None, storage=CommentsStorage())
    author = models.ForeignKey(SpaceoutUser, on_delete = models.CASCADE)
    content = models.ForeignKey(SpaceoutContent, on_delete = models.CASCADE)

class SpaceoutNotification(models.Model):
    NOTIFICATION_TYPE_COMMENT = 0
    NOTIFICATION_TYPES = (
     (NOTIFICATION_TYPE_COMMENT, 'Comment'),
    )

    type = models.IntegerField(default=0, choices=NOTIFICATION_TYPES)
    comment = models.ForeignKey(SpaceoutComment, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    user = models.ForeignKey(
        SpaceoutUser,
        on_delete = models.CASCADE,
        default = None,
    )

class WatsonInput(models.Model):
    SOCIAL_NETWORK_FACEBOOK = 0
    SOCIAL_NETWORK_TWITTER = 1
    SOCIAL_NETWORK_REDDIT = 2
    SOCIAL_NETWORK_SOUNDCLOUD = 3
    SOCIAL_NETWORK_TYPES = (
     (SOCIAL_NETWORK_FACEBOOK, 'Facebook'),
     (SOCIAL_NETWORK_TWITTER, 'Twitter'),
     (SOCIAL_NETWORK_REDDIT, 'Reddit'),
     (SOCIAL_NETWORK_SOUNDCLOUD, 'Sound Cloud'),
    )

    WATSON_RECIPE_LIKES = 0
    WATSON_RECIPE_SHARES = 1
    WATSON_RECIPE_POSTS = 2
    WATSON_RECIPE_EVENTS = 3
    WATSON_RECIPE_TYPE = (
     (WATSON_RECIPE_LIKES, 'Likes'),
     (WATSON_RECIPE_SHARES, 'Shares'),
     (WATSON_RECIPE_POSTS, 'Posts'),
     (WATSON_RECIPE_EVENTS, 'Events'),
    )

    recipe_id = models.IntegerField(choices=WATSON_RECIPE_TYPE)
    chunk_id = models.IntegerField()
    chunk_date_start = models.DateField()
    chunk_date_end = models.DateField()
    chunk_date_end = models.DateField()
    data_size = models.FloatField()
    social_network = models.IntegerField(default=0, choices=SOCIAL_NETWORK_TYPES)
    input_url = models.FileField(upload_to=watson_directory_path, default=None, storage=WatsonStorage())
    watson_response_time = models.FloatField()

    user = models.ForeignKey(
        SpaceoutUser,
        on_delete = models.CASCADE,
        default = None,
    )

class WatsonOutput(models.Model):

    WATSON_ANALYSIS_CONCEPTS = 0
    WATSON_ANALYSIS_KEYWORDS = 1
    WATSON_ANALYSIS_ENTITIES = 2
    WATSON_ANALYSIS_TYPES = (
     (WATSON_ANALYSIS_CONCEPTS, 'Concepts'),
     (WATSON_ANALYSIS_KEYWORDS, 'Keywords'),
     (WATSON_ANALYSIS_ENTITIES, 'Entities'),
    )

    analysis = models.IntegerField(default=0, choices=WATSON_ANALYSIS_TYPES)
    text = models.CharField(max_length=256, default='')
    relevance = models.FloatField()

    def model_callable(self):
        return self.text

    watson_input = models.ForeignKey(
        WatsonInput,
        on_delete = models.CASCADE,
        default = None,
    )
