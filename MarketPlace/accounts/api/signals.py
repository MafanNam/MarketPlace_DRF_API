from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import UserProfile


@receiver(post_save, sender=get_user_model())
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print('work')
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the user profile if not exist
            UserProfile.objects.create(user=instance)
