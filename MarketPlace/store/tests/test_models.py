from django.test import TestCase

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from ..models import (
    Product, ReviewRating, AttributeValue,
    Category, Brand, Attribute,
)


def create_product(
        seller_shop, category, brand, attribute_value,
        product_name='test_name', article='CD334',
        price_new=99, stock_qty=12):
    product = Product.objects.create(
        seller_shop=seller_shop, product_name=product_name,
        category=category, brand=brand,
        article=article, price_new=price_new, stock_qty=stock_qty)
    product.attribute_value.set([attribute_value])

    return product


class StoreTests(TestCase):

    def setUp(self) -> None:
        self.user_sel = create_user(
            username=fake.email().split('@')[0],
            email=fake.email(),
            is_active=True,
            role=1,
        )
        self.user_cus = create_user(
            username=fake.email().split('@')[0],
            email=fake.email(),
            is_active=True,
        )
        self.seller_shop = SellerShop.objects.get(owner=self.user_sel)
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

        seller_profile = SellerShop.objects.filter(owner=self.user_sel).exists()
        self.assertTrue(seller_profile)

        self.assertEqual(product.category, self.category)
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(
            product.attribute_value.get(product=product), self.attribute_value)
        self.assertEqual(product.get_attribute_value(), self.attribute_value.__str__())

        review = ReviewRating.objects.create(
            product=product, rating=5, user=self.user_cus
        )

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user_cus)

    def test_str_category(self):
        self.assertEqual(self.category.__str__(), 'test_cat1')

    def test_str_brand(self):
        self.assertEqual(self.brand.__str__(), 'test_brand1')

    def test_str_attribute(self):
        self.assertEqual(self.attribute.__str__(), 'color')

    def test_str_attribute_value(self):
        self.assertEqual(self.attribute_value.__str__(), 'color - red')

    def test_str_product(self):
        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value)
        self.assertEqual(product.__str__(), 'test_name')

    def test_str_rating(self):
        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value)
        rating = ReviewRating.objects.create(
            user=self.user_cus, product=product, rating=5
        )
        self.assertEqual(rating.__str__(), f'{rating.name}-5')
