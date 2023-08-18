import random
import string

from django.utils.text import slugify


def update_product_review(product):
    reviews = product.review.all()
    count_reviews = reviews.count()
    product.numReviews = count_reviews

    if count_reviews > 0:
        total = 0
        for rev in reviews:
            total += rev.rating

        product.rating = total / count_reviews
    else:
        product.rating = 0

    product.save()


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.product_name)
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug[:max_length - 5],
            randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_article_generator(instance):
    category_initials = ''.join(
        word[0] for word in instance.category.category_name.split())
    product_initials = instance.product_name.replace(' ', '')[:3]

    article = f"{category_initials}-{product_initials}" \
              f"{random_string_generator(size=6)}"

    return article
