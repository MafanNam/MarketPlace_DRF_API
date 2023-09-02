from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import SellerShop, User
from accounts.tests.test_views import create_user, fake
from cart.tests.test_models import create_cart
from cart.tests.test_views import create_cart_item
from orders.api.serializers import OrderSerializer
from orders.models import Order, Tax, OrderItem
from store.models import (
    Product, AttributeValue,
    Category, Brand, Attribute,
)

ORDER_URL = reverse('orders:orders-list')


def detail_order_url(order_id):
    """Create and return a order detail URL."""
    return reverse('orders:orders-detail', args=[order_id])


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


def create_order(
        user, tax, order_number='AD245'):
    order = Order.objects.create(
        user=user, tax=tax, payment_method='paypal',
        order_number=order_number)
    return order


class PublicOrderApiTests(TestCase):

    def test_list_orders_unauthorized(self):
        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_unauthorized(self):
        res = self.client.post(ORDER_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):

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
        self.user_cus2 = create_user(
            username=fake.email().split('@')[0],
            email=fake.email(),
            is_active=True,
            role=2,
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
        self.tax = Tax.objects.create(
            name_tax='test', value_tax='44.99', default=True)
        self.order = create_order(
            user=self.user_cus, tax=self.tax, order_number='DD333')
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=5)
        self.cart = create_cart(self.user_sel)
        self.cart_item = create_cart_item(
            cart=self.cart, product=self.product,
            attribute_value=self.attribute_value, quantity=2)
        self.cart2 = create_cart(self.user_cus2)
        self.cart_item2 = create_cart_item(
            cart=self.cart2, product=self.product,
            attribute_value=self.attribute_value, quantity=2)

    def test_list_order(self):
        res = self.client.get(ORDER_URL)

        orders = Order.objects.filter(user=self.user_cus)
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_order(self):
        url = detail_order_url(self.order.id)
        res = self.client.get(url)

        orders = Order.objects.get(user=self.user_cus, id=self.order.id)
        serializer = OrderSerializer(orders, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_order(self):
        self.client.force_authenticate(self.user_cus2)

        payload = {
            'cart_id': self.cart2.id,
            'payment_method': 'paypal',
            'order_note': '',
            'shipping_price': 44,
            'shipping_address': {
                "address": "string",
                "country": "string",
                "oblast": "string",
                "city": "string",
                "depart_num": "string"
            }
        }
        res = self.client.post(ORDER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['payment_method'], payload['payment_method'])
        self.assertEqual(
            res.data['shipping_address']['address'],
            payload['shipping_address']['address'])

    def test_delete_order(self):
        url = detail_order_url(self.order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        order = Order.objects.filter(user=self.user_cus)
        self.assertEqual(order.count(), 0)

    def test_partial_update_order(self):
        payload = {
            'status': 'C'
        }
        admin = User.objects.create_superuser('test@admin.com', 'testpass123')
        self.client.force_authenticate(admin)

        url = detail_order_url(self.order.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], payload['status'])
        order = Order.objects.get(user=self.user_cus)
        self.assertEqual(order.status, payload['status'])

    def test_order_pay_partial_update(self):
        url = reverse('orders:order_pay', args=[self.order.id])
        res = self.client.patch(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
