from django.test import TestCase

from accounts.models import SellerShop
from accounts.tests.test_views import fake, create_user
from cart.models import Cart, CartItem
from store.models import Category, Brand, Attribute, AttributeValue
from store.tests.test_views import create_product


def create_cart(user):
    return Cart.objects.create(user=user)


class CartTests(TestCase):

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

    def test_create_cart(self):
        cart = create_cart(user=self.user_cus)

        self.assertEqual(cart.__str__(), f"{cart.user}-{cart.total_price}")
        self.assertEqual(cart.user, self.user_cus)

    def test_create_cart_item(self):
        cart = create_cart(user=self.user_cus)

        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value
        )
        cart_item = CartItem.objects.create(
            cart=cart, product=product, attribute_value_id=1,
            quantity=3)

        self.assertEqual(
            cart_item.__str__(), f"{cart_item.product}-{cart_item.quantity}")
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.attribute_value.value, 'red')
        self.assertEqual(cart_item.quantity, 3)

    def test_delete_cart(self):
        cart = create_cart(user=self.user_cus)

        product = create_product(
            seller_shop=self.seller_shop, category=self.category,
            brand=self.brand, attribute_value=self.attribute_value
        )
        cart_item = CartItem.objects.create(
            cart=cart, product=product, attribute_value_id=1,
            quantity=3)

        cart.delete()

        cart_item = CartItem.objects.all().exists()
        self.assertFalse(cart_item)
        cart = Cart.objects.all().exists()
        self.assertFalse(cart)
