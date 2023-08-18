from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .utils import unique_slug_generator_seller
from ..models import UserProfile, SellerShop


@receiver(post_save, sender=get_user_model())
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    user = sender.objects.get(id=instance.id)
    if user.role == 2 and not user.is_staff:
        if created:
            UserProfile.objects.create(user=instance)
        else:
            try:
                profile = UserProfile.objects.get(user=instance)
                profile.save()
            except UserProfile.DoesNotExist:
                # Create the user profile if not exist
                UserProfile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def post_save_create_seller_shop_profile_receiver(sender, instance,
                                                  created, **kwargs):
    user = sender.objects.get(id=instance.id)
    if user.role == 1 and not user.is_staff:
        if created:
            SellerShop.objects.create(owner=instance)
        else:
            try:
                seller_shop = SellerShop.objects.get(owner=instance)
                seller_shop.save()
            except SellerShop.DoesNotExist:
                # Create the Seller Shop profile if not exist
                SellerShop.objects.create(owner=instance)


@receiver(pre_save, sender=SellerShop)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_seller(instance)
