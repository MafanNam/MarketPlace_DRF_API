import random
import string

from django.utils.text import slugify
from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_verification_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'],
            to=(data['to_email'],))
        email.send()


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_seller(instance, new_slug=None):
    if new_slug is not None:
        slug = slugify(new_slug)
    else:
        slug = slugify(instance.shop_name)
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}{randstr}".format(
            slug=slug[:max_length - 5],
            randstr=random_string_generator())

        return unique_slug_generator_seller(instance, new_slug=new_slug)
    return slug
