from django.dispatch import receiver
from django.db.models.signals import post_delete

from spaceoutvr.models import SpaceoutComment

@receiver(post_delete, sender=SpaceoutComment)
def delete_file(sender, instance, *args, **kwargs):
    instance.audio_file.storage.delete(instance.audio_file.name)