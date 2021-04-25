from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from clothes import models
from clothes.tests.test_clothes_models import (sample_brand, sample_category,
                                               sample_subcategory, sample_shop)


def create_other_user():
    other_user = get_user_model().objects.create_user(
            email='hana.kikuchi@gmail.com',
            password='password1023'
        )
    return other_user


class Cloths_Model_Test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='kikuchi.dai@gmail.com',
            password='password'
        )

    def test_brand_listing_for_logged_in_user(self):
        """Test list view of Brand objects for logged in user"""
        self.client.force_login(self.user)
        other_user = create_other_user()
        # Create brand object with logged_in user
        sample_brand(self.user, name='Lardini')
        # Create brand object with other_user
        sample_brand(user=other_user, name='Gransasso')
        response = self.client.get(reverse('clothes:brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini')
        self.assertTemplateUsed(response, 'brand/brand_list.html')
        self.assertEqual(len(response.context['brand_list']), 1)

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
        self.client.force_login(self.user)
        other_user = create_other_user()

        # Create clothe object with logged_in user
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

        # Create clothe object with other_user
        models.Clothes.objects.create(
            user=other_user,
            name='Gransasso Knit',
            price=22000,
            description='Gransassoのシャツジャケット',
            brand=sample_brand(user=other_user, name='Gransasso'),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(other_user, name='ModernBlue'),
            purchased=timezone.now(),
        )
        response = self.client.get(reverse('clothes:brand_clothes',
                                   kwargs={'id': brand.id,
                                           'slug': brand.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertTemplateUsed(response, 'brand/brand_clothes_list.html')
        self.assertEqual(len(response.context['brand_clothes_list']), 1)

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
            '%s?next=/clothes/brand/%s/%s/'
            % (reverse('account_login'), brand.id, brand.slug))
        self.assertContains(response, 'ログイン')

    def test_category_listing_for_logged_in_user(self):
        """Test list view of Category objects for logged in user"""
        self.client.force_login(self.user)
        other_user = create_other_user()
        # Create category object with logged_in user
        sample_category(user=self.user)
        # Create category object with other_user
        sample_category(user=other_user, name='Knit')
        response = self.client.get(reverse('clothes:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jacket')
        self.assertTemplateUsed(response, 'category/category_list.html')
        self.assertEqual(len(response.context['category_list']), 1)

    def test_category_listing_for_logged_out_user(self):
        """
        Test accessing to list view of category objects with logged out user
        """
        response = self.client.get(reverse('clothes:category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/category/'
             % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/clothes/category/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_category_clothes_listing_for_logged_in_user(self):
        """Test listing of clothes of a Category for logged in user"""
        self.client.force_login(self.user)
        category = sample_category(self.user)
        # Create clothe object with logged_in user
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
        other_user = create_other_user()
        # Create clothe object with other_user
        models.Clothes.objects.create(
            user=other_user,
            name='Gransasso Knit',
            price=22000,
            description='Gransassoのシャツジャケット',
            brand=sample_brand(user=other_user, name='Gransasso'),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(other_user, name='ModernBlue'),
            purchased=timezone.now(),
        )
        response = self.client.get(reverse('clothes:category_clothes',
                                   kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertTemplateUsed(response,
                                'category/category_clothes_list.html')
        self.assertEqual(len(response.context['category_clothes_list']), 1)

    def test_category_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to category clothes list view"""
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

    def test_shop_listing_for_logged_in_user(self):
        """Test list view of Shop objects for logged in user"""
        self.client.force_login(self.user)
        other_user = create_other_user()
        # Create shop object with logged_in user
        sample_shop(self.user)
        # Create shop object with other_user
        sample_shop(user=other_user, name='Ships')
        response = self.client.get(reverse('clothes:shop_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beams')
        self.assertTemplateUsed(response, 'shop/shop_list.html')
        # Only shop created by logged_in_user is in the list
        self.assertEqual(len(response.context['shop_list']), 1)

    def test_shop_listing_for_logged_out_user(self):
        """Test accessing to list view of shop objects with logged out user"""
        response = self.client.get(reverse('clothes:shop_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/shop/'
             % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/clothes/shop/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_shop_clothes_listing_for_logged_in_user(self):
        """Test listing of clothes of a shop for logged in user"""
        category = sample_category(self.user)
        shop = sample_shop(self.user)
        self.client.force_login(self.user)
        other_user = create_other_user()

        # Create clothes object with logged_in user
        models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=sample_brand(self.user),
            sub_category=sample_subcategory(category=category),
            shop=shop,
            purchased=timezone.now(),
        )

        # Create clothes object with other_user
        models.Clothes.objects.create(
            user=other_user,
            name='Gransasso Knit',
            price=22000,
            description='Gransassoのシャツジャケット',
            brand=sample_brand(user=other_user, name='Gransasso'),
            sub_category=sample_subcategory(category=category),
            shop=shop,
            purchased=timezone.now(),
        )
        response = self.client.get(reverse('clothes:shop_clothes',
                                   kwargs={'slug': shop.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertTemplateUsed(response, 'shop/shop_clothes_list.html')
        # Only clothes of shop created by logged_in_user is in the list
        self.assertEqual(len(response.context['shop_clothes_list']), 1)

    def test_shop_clothes_listing_for_logged_out_user(self):
        """Test for logged_out_user to access to shop's clothes list view"""
        shop = sample_shop(self.user)
        response = self.client.get(reverse('clothes:shop_clothes',
                                   kwargs={'slug': shop.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/clothes/shop/%s/'
             % (reverse('account_login'), shop.slug))
        response = self.client.get(
            '%s?next=/clothes/shop/%s/'
            % (reverse('account_login'), shop.slug))
        self.assertContains(response, 'ログイン')

    def test_clothes_listing_for_logged_in_user(self):
        """Test list view of clothe objects for logged in user on"""
        self.client.force_login(self.user)
        other_user = create_other_user()

        category = sample_category(self.user)

        # Create clothes object with logged_in user
        models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=sample_brand(self.user),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(user=self.user),
            purchased=timezone.now(),
        )

        # Create clothes object with other_user
        models.Clothes.objects.create(
            user=other_user,
            name='Gransasso Knit',
            price=22000,
            description='Gransassoのシャツジャケット',
            brand=sample_brand(user=other_user, name='Gransasso'),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(user=other_user, name='Ships'),
            purchased=timezone.now(),
        )
        response = self.client.get(reverse('clothes_list_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lardini')
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(response.context['clothes_list']), 1)

    def test_clothes_listing_for_logged_out_user(self):
        """
        Test accessing to list view of Clothes objects with logged out user
        """
        response = self.client.get(reverse('clothes_list_home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
             response, '%s?next=/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/' % (reverse('account_login')))
        self.assertContains(response, 'ログイン')

    def test_clothes_detail_view(self):
        self.client.force_login(self.user)

        category = sample_category(self.user)

        # Create clothes object with logged_in user
        self.clothes = models.Clothes.objects.create(
            user=self.user,
            name='Lardini shirt Jacket',
            price=35000,
            description='ラルディーニのシャツジャケット',
            brand=sample_brand(self.user),
            sub_category=sample_subcategory(category=category),
            shop=sample_shop(user=self.user),
            purchased=timezone.now(),
        )
        response = self.client.get(self.clothes.get_absolute_url())
        no_response = self.client.get('/clothes/19/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Lardini shirt Jacket')
        self.assertContains(response, 'ラルディーニのシャツジャケット')
        self.assertTemplateUsed(response, 'clothes/clothes_detail.html')
