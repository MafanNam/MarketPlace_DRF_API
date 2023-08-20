from django.test import TestCase

from accounts.models import SellerShop
from ..models import (
    News, About, Main, Licence,
)


class AddonsModelTests(TestCase):

    def test_str_news(self):
        news = News.objects.create(title='test', text='description')

        self.assertEqual(news.__str__(), 'test')

    def test_str_about(self):
        about = About.objects.create(name='test', text='description')

        self.assertEqual(about.__str__(), 'test')

    def test_str_licence(self):
        licence = Licence.objects.create(name='test', text='description')

        self.assertEqual(licence.__str__(), 'test')

    def test_str_main(self):
        main = Main.objects.create(name='test', text='description')

        self.assertEqual(main.__str__(), 'test')


