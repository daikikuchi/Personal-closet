from django.utils import timezone
from unittest.mock import patch

from django.test import TestCase
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
        self.brand = models.Brand.objects.create(
            user=self.user,
            name='Lardini',
            description='世界の名だたるメゾンの製品を30年以上作り続けてきた「LARDINI」'
        )

        self.sub_category = models.SubCategory.objects.create(
            name='Casual Jacket',
            category=self.category,
        )

        self.shop = models.Shop.objects.create(
            name='Moden Blue',
            url='https://www.rakuten.ne.jp/gold/mb/rk/',
            user=self.user,
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
        self.assertEqual(str(self.brand), self.brand.name)

    def test_category_str(self):
        """Test the category strung representation"""
        self.assertEqual(str(self.category), self.category.name)

    def test_sub_category_str(self):
        """Test the sub category string representation"""
        self.assertEqual(str(self.sub_category),
                         f'{self.sub_category.category} - {self.sub_category.name}')

    def test_shop_str(self):
        """Test the shop string representation"""
        self.assertEqual(str(self.shop), self.shop.name)

    def test_clothes_str(self):
        """Test clothing representation"""
        clothes = models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt jaket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            purchased=timezone.now(),
            brand=self.brand,
            shop=self.shop,
            sub_category=self.sub_category
        )

        self.assertEqual(str(clothes), clothes.name)

    @patch('uuid.uuid4')
    def test_clothes_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.clothes_image_file_path(None, 'myimage.jpg')
        exp_path = f'clothes/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
