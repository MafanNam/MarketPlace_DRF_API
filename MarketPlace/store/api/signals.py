from django.db.models.signals import pre_save
from django.dispatch import receiver

from store.api.utils import unique_slug_generator, unique_article_generator
from store.models import Product


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.article:
        instance.article = unique_article_generator(instance)
