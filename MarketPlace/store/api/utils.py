import uuid

from django.template.defaultfilters import slugify


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


def generate_article(product_name, category_name):
    category_initials = ''.join(
        word[0] for word in category_name.split())
    product_initials = product_name.replace(' ', '')[:3]
    article = f"{category_initials}-{product_initials}{str(uuid.uuid4())[:4]}"

    return article


def generate_slug(title: str, pk: int):
    title = f"{slugify(title)}-{pk}"

    return title
