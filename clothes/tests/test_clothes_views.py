from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from clothes import models
from clothes.tests.test_clothes_models import (sample_brand, sample_category,
                                               sample_subcategory, sample_shop)


class Cloths_Model_Test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='kikuchi.dai@gmail.com',
            password='password'
        )

    def test_brand_listing_for_logged_in_user(self):
        """Test list view of Brand objects for logged in user"""
        sample_brand(self.user, name='Lardini')

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
        category = sample_category(self.user)
        brand = sample_brand(self.user, name='Lardini')
        models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=brand,
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(self.user),
            purchased=timezone.now(),
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:brand_clothes',
                                   kwargs={'id': brand.id,
                                           'slug': brand.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertTemplateUsed(response, 'brand/brand_clothes_list.html')

    def test_brand_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to brand clotes list view"""
        brand = sample_brand(user=self.user)
        response = self.client.get(reverse('clothes:brand_clothes',
                                   kwargs={'id': brand.id,
                                           'slug': brand.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/brand/%s/%s/'
             % (reverse('account_login'), brand.id, brand.slug))
        response = self.client.get(
            '%s?next=/clothes/brand/2/lardini/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_category_listing_for_logged_in_user(self):
        """Test list view of Category objects for logged in user"""
        sample_category(user=self.user)
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
        category = sample_category(self.user)
        models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=sample_brand(self.user),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(self.user),
            purchased=timezone.now(),
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('clothes:category_clothes',
                                   kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')

    def test_category_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to category clotes list view"""
        category = sample_category(self.user)
        response = self.client.get(reverse('clothes:category_clothes',
                                   kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/category/%s/'
             % (reverse('account_login'), category.slug))
        response = self.client.get(
            '%s?next=/clothes/category/%s/'
            % (reverse('account_login'), category.slug))
        self.assertContains(response, 'ログイン')
