from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from cart.models import (
    CartItem, Cart
)
from cart.tests.test_models import create_cart
from store.models import Category, Brand, Attribute, AttributeValue
from store.tests.test_views import create_product

CART_URL = reverse('cart:cart-list')


def list_cart_items_url(cart_id):
    """Create and return a cart items list URL."""
    return reverse('cart:cart-items-list', args=[cart_id])


def detail_cart_items_url(cart_id, item_id):
    """Create and return a cart items detail URL."""
    return reverse('cart:cart-items-detail', args=[cart_id, item_id])


def detail_cart_url(cart_id):
    """Create and return a cart detail URL."""
    return reverse('cart:cart-detail', args=[cart_id])


def create_cart_item(cart, product, attribute_value, quantity):
    return CartItem.objects.create(
        cart=cart, product=product, attribute_value=attribute_value,
        quantity=quantity)


class PublicCartApiTests(TestCase):

    def test_list_cart_unauthorized_error(self):
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_cart_item_unauthorized_error(self):
        cart = create_cart(user=create_user())
        url = detail_cart_url(cart.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCartApiTests(TestCase):

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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_cus)
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
        self.cart = create_cart(self.user_cus)
        self.cart_item = create_cart_item(
            cart=self.cart, product=self.product,
            attribute_value=self.attribute_value, quantity=2)

    def test_list_cart(self):
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_cart_detail(self):
        url = detail_cart_url(self.cart.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_cart_item(self):
        url = list_cart_items_url(self.cart.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_detail_cart_item(self):
        url = detail_cart_items_url(self.cart.id, self.cart_item.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['quantity'], self.cart_item.quantity)

    def test_create_cart(self):
        self.client.force_authenticate(self.user_sel)
        res = self.client.post(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], self.user_sel.id)

    def test_create_cart_item(self):
        payload = {
            'product': 1,
            'quantity': 4,
            'attribute_value': 1
        }
        res = self.client.post(list_cart_items_url(self.cart.id), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.cart_item.refresh_from_db()
        self.assertEqual(
            res.data['quantity'], self.cart_item.quantity)
        self.assertEqual(res.data['attribute_value'], self.attribute_value.id)
        self.assertEqual(res.data['product'], self.product.id)

    def test_update_cart_item(self):
        payload = {
            'quantity': 8,
        }
        res = self.client.patch(
            detail_cart_items_url(self.cart.id, self.cart_item.id), payload)

        self.cart_item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data['quantity'], self.cart_item.quantity)

    def test_delete_cart(self):
        url = detail_cart_url(self.cart.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        cart_item = CartItem.objects.all().exists()
        self.assertFalse(cart_item)
        cart = Cart.objects.all().exists()
        self.assertFalse(cart)

    def test_delete_cart_item(self):
        url = detail_cart_items_url(self.cart.id, self.cart_item.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        cart_item = CartItem.objects.all().exists()
        self.assertFalse(cart_item)
        cart = Cart.objects.all().exists()
        self.assertTrue(cart)
