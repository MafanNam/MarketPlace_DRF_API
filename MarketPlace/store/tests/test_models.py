from django.test import TestCase

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from ..models import (
    Product, ReviewRating, AttributeValue,
    Category, Brand, Attribute,
)


def create_product(
        seller_shop=1, product_name='test_name',
        category=1, brand=1, attribute_value=1,
        article='CD334', price_new=99, stock_qty=12, ):
    product = Product.objects.create(
        seller_shop=seller_shop, product_name=product_name,
        category=category, brand=brand,
        article=article, price_new=price_new, stock_qty=stock_qty)
    product.attribute_value.set([attribute_value])

    return product


class StoreTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            first_name='test_first',
            last_name='test_last',
            username=fake.email().split('@')[0],
            email=fake.email(),
            password='testpass123',
            phone_number='+343 2424 5345',
            is_active=True,
            role=1,
        )
        self.seller_shop = SellerShop.objects.get(owner=self.user)
        self.category = Category.objects.create(category_name='test_cat1')
        self.brand = Brand.objects.create(brand_name='test_brand1')
        self.attribute = Attribute.objects.create(name='color')
        self.attribute_value = AttributeValue.objects.create(
            value='red', attribute=self.attribute)

    def test_create_product_and_related(self):
        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value
        )

        self.assertEqual(product.product_name, 'test_name')

        seller_profile = SellerShop.objects.filter(owner=self.user).exists()
        self.assertTrue(seller_profile)

        self.assertEqual(product.category, self.category)
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(
            product.attribute_value.get(product=product), self.attribute_value)

        review = ReviewRating.objects.create(
            product=product, rating=5, user=self.user
        )

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user)
