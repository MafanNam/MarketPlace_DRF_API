from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from ..models import (
    Product, AttributeValue,
    Category, Brand, Attribute, ReviewRating,
)
from rest_framework.test import APIClient

PRODUCT_URL = reverse('store:product-list')


def detail_product_url(product_slug):
    """Create and return a product detail URL."""
    return reverse('store:product-detail', args=[product_slug])


def detail_review_url(product_slug):
    """Create and return a product detail URL."""
    return reverse('store:review', args=[product_slug])


def create_product(
        seller_shop, category, brand, attribute_value,
        product_name='test_name',
        price_new=99, stock_qty=12):
    product = Product.objects.create(
        seller_shop=seller_shop, product_name=product_name,
        category=category, brand=brand,
        price_new=price_new, stock_qty=stock_qty)
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
            role=2,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_sel)
        self.seller_shop = SellerShop.objects.get(owner=self.user_sel)
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

    def test_product_create(self):
        payload = {
            'product_name': 'hh',
            'category': 1, 'brand': 1,
            'attribute_value': [1],
            'price_new': 5,
            'stock_qty': 12,
        }
        res = self.client.post(PRODUCT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(product_name=payload['product_name'])
        self.assertTrue(product.seller_shop, self.seller_shop)
        self.assertEqual(product.price_old, payload['price_new'])

    def test_product_update(self):
        payload = {
            'product_name': 'update_name',
            'price_new': 999,
        }
        price_old = self.product.price_new

        url = detail_product_url(self.product.slug)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product = Product.objects.filter(product_name=payload['product_name'])
        self.assertTrue(product.exists())
        self.assertEqual(product[0].product_name, payload['product_name'])
        self.assertTrue(product[0].seller_shop, self.seller_shop)
        self.assertEqual(product[0].price_old, price_old)

    def test_product_delete(self):
        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value,
            product_name='test_delete'
        )

        url = detail_product_url(product.slug)
        res = self.client.delete(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        product = Product.objects.filter(product_name=product.product_name)
        self.assertFalse(product.exists())

    def test_create_review_for_product_except(self):
        payload = {
            'rating': 3,
            'comment': 'test com',
        }
        url = detail_review_url(self.product.slug)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review = ReviewRating.objects.all().exists()

        self.assertFalse(review)

    def test_create_review_for_product(self):
        payload = {
            'rating': 3,
            'comment': 'test com',
        }
        url = detail_review_url(self.product.slug)
        self.client.force_authenticate(self.user_cus)
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        review = ReviewRating.objects.get(product=self.product)
        self.assertEqual(review.rating, payload['rating'])

        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, review.rating)
        self.assertEqual(self.product.numReviews, 1)

    def test_update_review_for_product(self):
        ReviewRating.objects.create(
            user=self.user_cus, product=self.product,
            rating=1,
        )
        payload = {
            'rating': 5,
            'comment': '',
        }
        url = detail_review_url(self.product.slug)
        self.client.force_authenticate(self.user_cus)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        review = ReviewRating.objects.get(product=self.product)
        self.assertEqual(review.rating, payload['rating'])

        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, review.rating)
        self.assertEqual(self.product.numReviews, 1)

    def test_delete_review_for_product(self):
        ReviewRating.objects.create(
            user=self.user_cus, product=self.product,
            rating=1,
        )
        url = detail_review_url(self.product.slug)
        self.client.force_authenticate(self.user_cus)
        res = self.client.delete(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        review = ReviewRating.objects.filter(product=self.product).exists()
        self.assertFalse(review)

        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 0)
        self.assertEqual(self.product.numReviews, 0)
