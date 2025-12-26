from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.
class AccountAppTest(TestCase):

    def test_user_can_register(self):
        response = self.client.post(reverse('signup'),
                                    {'phone':'09123040501','fullname':'Ali','password':'1234','confirm_password':'1234'})
        
        self.assertEqual(response.status_code,302)
        self.assertTrue(User.objects.filter(phone='09123040501').exists())
    
    def test_user_can_login(self):
        User.objects.create_user(phone='09123040501',password='1234')

        response = self.client.post(reverse('login'),{'phone-number':'09123040501','password':'1234'})

        self.assertEqual(response.status_code,302)
        
    def test_user_can_login(self):
        User.objects.create_user(phone='09123040501',password='1234')

        response = self.client.post(reverse('login'),{'phone-number':'09123040501','password':'wrong'})

        self.assertEqual(response.status_code,200)
        self.assertContains(response,'نام کاربری یا رمز عبور اشتباه است')
    
    def test_logout_user(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code,302)
    
    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse('tasks'))

        self.assertEqual(response.status_code,302)
        self.assertIn('login/',response.url)