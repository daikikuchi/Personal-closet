from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from clothes import models


class Tag_Model_Test(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='kikuchi.dai@gmail.com',
            password='password'
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
        print(type(brand))
        print(type(str(brand)))
        self.assertEqual(str(brand), brand.name)
