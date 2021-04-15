from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from clothes import models


def sample_brand(user, name='Lardini'):
    return models.Brand.objects.create(
            user=user,
            name=name
        )


def sample_category(user, name='Jacket'):
    return models.Category.objects.create(
        user=user,
        name=name
    )


def sample_subcategory(category, name='casual jacket'):
    return models.SubCategory.objects.create(
            name=name,
            category=category,
        )


def sample_shop(user, name='beams', url='https://beams.com'):
    return models.Shop.objects.create(
        user=user,
        name=name
    )


class Cloths_Model_Test(TestCase):

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
        brand = sample_brand(
            user=self.user
        )
        self.assertEqual(str(brand), brand.name)

    def test_category_str(self):
        """Test the category strung representation"""
        category = sample_category(
            user=self.user,
        )
        self.assertEqual(str(category), category.name)

    def test_sub_category_str(self):
        """Test the sub category string representation"""
        category = sample_category(
            user=self.user,
            name='Jacket'
        )
        sub_category = sample_subcategory(
            category=category
        )
        self.assertEqual(str(sub_category),
                         f'{sub_category.category} - {sub_category.name}')

    def test_shop_str(self):
        """Test the shop string representation"""
        shop = sample_shop(
            user=self.user
        )
        self.assertEqual(str(shop), shop.name)

    def test_clothes_str(self):
        """Test clothing representation"""
        category = sample_category(
            user=self.user,
        )
        clothes = models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=sample_brand(user=self.user),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(user=self.user),
            purchased=timezone.now(),
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
