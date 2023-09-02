from django.test import TestCase

from accounts.models import SellerShop
from accounts.tests.test_views import create_user, fake
from store.models import (
    Product, AttributeValue,
    Category, Brand, Attribute,
)
from orders.models import (
    Tax, Order, OrderItem, ShippingAddress
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


def create_order(
        user, tax, order_number='AD245'):
    order = Order.objects.create(
        user=user, tax=tax, payment_method='paypal',
        order_number=order_number)
    return order


class OrderTests(TestCase):

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
        self.product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value
        )

    def test_create_tax(self):
        tax = Tax.objects.create(
            name_tax='test', value_tax='44.99', default=True)

        self.assertEqual(tax.value_tax, '44.99')
        self.assertEqual(tax.name_tax, 'test')
        self.assertEqual(tax.__str__(), 'test-44.99')

    def test_create_order(self):
        tax = Tax.objects.create(
            name_tax='test', value_tax='44.99', default=True)
        order = create_order(
            user=self.user_cus, tax=tax, order_number='DD333')

        self.assertEqual(order.tax.value_tax, tax.value_tax)
        self.assertEqual(order.user, self.user_cus)
        self.assertEqual(order.__str__(), 'DD333')

    def test_create_order_item(self):
        tax = Tax.objects.create(
            name_tax='test', value_tax='44.99', default=True)
        order = create_order(
            user=self.user_cus, tax=tax, order_number='DD333')
        item = OrderItem.objects.create(
            order=order, product=self.product, quantity=5)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.order, order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.__str__(), f"{order}-{self.product}")

    def test_create_shipping_address(self):
        tax = Tax.objects.create(
            name_tax='test', value_tax='44.99', default=True)
        order = create_order(
            user=self.user_cus, tax=tax, order_number='DD333')
        shipping = ShippingAddress.objects.create(
            order=order, address='test', country='coun',
            oblast='obl', city='city', depart_num='333'
        )

        self.assertEqual(shipping.order, order)
        self.assertEqual(shipping.address, 'test')
        self.assertEqual(shipping.depart_num, '333')
        self.assertEqual(shipping.__str__(), 'test')

        self.assertEqual(order.address.address, 'test')
