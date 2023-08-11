from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import UserProfile, SellerShop


@receiver(post_save, sender=get_user_model())
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
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
    if created:
        SellerShop.objects.create(owner=instance)
    else:
        try:
            seller_shop = SellerShop.objects.get(owner=instance.id)
            seller_shop.save()
        except SellerShop.DoesNotExist:
            # Create the Seller Shop profile if not exist
            SellerShop.objects.create(owner=instance)
