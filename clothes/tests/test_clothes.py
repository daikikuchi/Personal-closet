from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from clothes import models


class Cloths_Model_Test(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='kikuchi.dai@gmail.com',
            password='password'
        )

        self.category = models.Category.objects.create(
            user=self.user,
            name='Jacket',
        )

    def test_tag_str(self):
        """Test the tag string reprsentation"""
        tag = models.Tag.objects.create(
            user=self.user,
            name='Knit'
        )
        self.assertEqual(str(tag), tag.name)

    def test_brand_str(self):
        """Test the brand string representation"""
        brand = models.Brand.objects.create(
            user=self.user,
            name='Gran Sasso',
            description='Gran Sasso（グランサッソ）は1952年サンテジーディオ・アッラ・ヴィブラータ\
            という小さな村で、起業精神あふれる4人の兄弟により設立されました。'
        )
        self.assertEqual(str(brand), brand.name)

    def test_category_str(self):
        """Test the category strung representation"""
        self.assertEqual(str(self.category), self.category.name)

    def test_sub_category_str(self):
        """Test the sub category string reprsenation"""
        sub_category = models.SubCategory.objects.create(
            name='Casual Jacket',
            category=self.category,
        )
        self.assertEqual(str(sub_category),
                         f'{sub_category.category} - {sub_category.name}')

    def test_shop_str(self):
        """Test the sho[] category string reprsenation"""
        shop = models.Shop.objects.create(
            name='Moden Blue',
            url='https://www.rakuten.ne.jp/gold/mb/rk/',
            user=self.user,
        )
        self.assertEqual(str(shop), shop.name)
