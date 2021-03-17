from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class Custom_User_Model_Test(TestCase):

    def test_create_user_with_emails(self):
        """Test that successfully create a user with an emaill """
        email = 'test@gmail.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        """"Test that email for a new user is normalized"""
        email = 'test@GMAIL.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """"Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpassword')

    def test_create_new_superuser(self):
        """Test creating a new superiser"""
        email = 'test@gmail.com'
        password = 'testpassword'
        admin_user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test_admin@gmail.com',
            password='adminpassword'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='userpassword',
            name='User for test'
        )

    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse('admin:accounts_customuser_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:accounts_customuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:accounts_customuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


class SignUpPageTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        """Test that singup template is rendered correctly"""
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'I am not on this page!')
