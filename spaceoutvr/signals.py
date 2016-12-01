from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from spaceoutvr.models import SpaceoutUser, SpaceoutComment, SpaceoutNotification, WatsonInput
from spaceoutvr.notifications import OneSignalNotifications

@receiver(post_delete, sender=SpaceoutComment)
def delete_file(sender, instance, *args, **kwargs):
    instance.audio_file.storage.delete(instance.audio_file.name)

@receiver(post_delete, sender=WatsonInput)
def delete_file(sender, instance, *args, **kwargs):
    instance.input_url.storage.delete(instance.input_url.name)

@receiver(post_delete, sender=SpaceoutUser)
def delete_file(sender, instance, *args, **kwargs):
    instance.personality_insights_input_url.storage.delete(instance.personality_insights_input_url.name)
    instance.personality_insights_output_url.storage.delete(instance.personality_insights_output_url.name)

@receiver(post_save, sender=SpaceoutComment)
def add_subscriber(sender, instance, *args, **kwargs):
    # add a notification for each user in the comment thread
    # members = SpaceoutContent.objects.filter(commenters__id = 1)
    members = instance.content.members()
    for member in members:
        notification = SpaceoutNotification()
        notification.type = SpaceoutNotification.NOTIFICATION_TYPE_COMMENT
        notification.comment = instance
        notification.user = member
        notification.save()


@receiver(post_save, sender=SpaceoutNotification)
def push_notification(sender, instance, created, *args, **kwargs):
    if created:
        n = OneSignalNotifications()
        n.send(instance.user)
