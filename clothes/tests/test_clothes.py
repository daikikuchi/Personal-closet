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
