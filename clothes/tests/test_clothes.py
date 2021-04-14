from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from clothes import models


class Cloths_Model_Test(TestCase):

    def setUp(self):
        self.client = Client()

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

        self.clothes = models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            purchased=timezone.now(),
            brand=self.brand,
            shop=self.shop,
            sub_category=self.sub_category
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
        self.assertEqual(str(self.clothes), self.clothes.name)

    @patch('uuid.uuid4')
    def test_clothes_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.clothes_image_file_path(None, 'myimage.jpg')
        exp_path = f'clothes/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_brand_listing_for_logged_in_user(self):
        """Test list view of Brand objects for logged in user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini')
        self.assertTemplateUsed(response, 'brand/brand_list.html')

    def test_brand_listing_for_logged_out_user(self):
        """Test accessing to list view of Brand objects with logged out user"""
        response = self.client.get(reverse('clothes:brand_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/brand/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/clothes/brand/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_brand_clothes_listing_for_logged_in_user(self):
        """Test listing of clothes of a brand for logged in user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:brand_clothes',
                                   kwargs={'id': self.brand.id,
                                           'slug': self.brand.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertTemplateUsed(response, 'brand/brand_clothes_list.html')

    def test_brand_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to brand clotes list view"""
        response = self.client.get(reverse('clothes:brand_clothes',
                                   kwargs={'id': self.brand.id,
                                           'slug': self.brand.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response,
             '%s?next=/clothes/brand/2/lardini/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/clothes/brand/2/lardini/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_category_listing_for_logged_in_user(self):
        """Test list view of Category objects for logged in user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jacket')
        self.assertTemplateUsed(response, 'category/category_list.html')

    def test_category_listing_for_logged_out_user(self):
        """Test accessing to list view of Brand objects with logged out user"""
        response = self.client.get(reverse('clothes:category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/category/'
             % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/clothes/brand/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_category_clothes_listing_for_logged_in_user(self):
        """Test listing of clothes of a Category for logged in user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:category_clothes',
                                   kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')

    def test_category_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to category clotes list view"""
        response = self.client.get(reverse('clothes:category_clothes',
                                   kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/category/%s/'
             % (reverse('account_login'), self.category.slug))
        response = self.client.get(
            '%s?next=/clothes/category/%s/'
            % (reverse('account_login'), self.category.slug))
        self.assertContains(response, 'ログイン')
