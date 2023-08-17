from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from ..models import Product, ReviewRating, AttributeValue, Category, Brand, Attribute
from rest_framework.test import APIClient

PRODUCT_URL = reverse('store:product-list')


def create_product(
        seller_shop=1, product_name='test_name',
        category=1, brand=1, attribute_value=1,
        article='CD334', price_new=99, stock_qty=12):
    product = Product.objects.create(
        seller_shop=seller_shop, product_name=product_name,
        category=category, brand=brand,
        article=article, price_new=price_new, stock_qty=stock_qty)
    product.attribute_value.set([attribute_value])

    return product


class PublicStoreApiTests(TestCase):

    def test_create_product_unauthorized(self):
        res = self.client.post(PRODUCT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_retrieve_unauthorized(self):
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateStoreApiTests(TestCase):

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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.seller_shop = SellerShop.objects.get(owner=self.user)
        self.category = Category.objects.create(category_name='test_cat1')
        self.brand = Brand.objects.create(brand_name='test_brand1')
        self.attribute = Attribute.objects.create(name='color')
        self.attribute_value = AttributeValue.objects.create(
            value='red', attribute=self.attribute)
        self.product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value
        )

    def test_product_create_without_data(self):
        res = self.client.post(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_product_create(self):
    #     payload = {
    #         'seller_shop': 1, 'product_name': 'hh',
    #         'category': 1, 'brand': 1,
    #         'attribute_value': [1],
    #         'article': 'CD3354', 'price_new': 99, 'stock_qty': 12
    #     }
    #     res = self.client.post(PRODUCT_URL, payload, format='json')
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
