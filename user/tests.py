from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    
    # def test_register(self):
    #     data = {
    #         'username': 'testcase',
    #         'email': 'testcase@example.com',
    #         'password' : 'NewPassword@123',
    #         'password2' : 'NewPassword@123'
    #     }
        
    #     response = self.client.post(reverse('register'), data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual( User.objects.count(),1)
    
    def setUp(self):
        self.url = reverse("register")

        self.valid_data = {
            "username": "romman",
            "email": "romman@gmail.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123",
        }


    def test_register_successfully(self):

        response = self.client.post(self.url,self.valid_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        self.assertTrue(User.objects.filter(username="romman").exists())


    def test_duplicate_username(self):

        User.objects.create_user(
            username="romman",
            email="abc@gmail.com",
            password="12345678",
            
        )

        response = self.client.post(self.url,self.valid_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("username",response.data)


    def test_duplicate_email(self):

        User.objects.create_user(
            username="another_user",
            email="romman@gmail.com",
            password="12345678",
            
        )

        response = self.client.post(self.url,self.valid_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("email",response.data)


    def test_missing_password(self):

        data = self.valid_data.copy()
        data.pop("password")

        response = self.client.post(self.url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("password",response.data)


    def test_invalid_email(self):

        data = self.valid_data.copy()
        data["email"] = "invalid-email"

        response = self.client.post(self.url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("email",response.data)


    def test_empty_request(self):

        response = self.client.post(self.url,{},format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("username",response.data)
        self.assertIn("email",response.data)
        self.assertIn("password",response.data)


    def test_password_is_hashed(self):

        self.client.post(self.url,self.valid_data,format="json")
        user = User.objects.get(username="romman")
        self.assertTrue(user.check_password("StrongPassword123"))
        
        
class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.url = reverse("login")
        self.username = 'romman'
        self.password= 'StrongPassword123'
        
        self.user = User.objects.create_user(
            username= self.username,
            password= self.password
        )
        
    def test_login(self):
        data = {
            'username': self.username,
            'password' : self.password
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        
    
    def test_wrong_password(self):
        data = {
            'username': self.username,
            'password' : 'jduhdullem'
        }       
        response = self.client.post(self.url, data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_wrong_username(self):
        data = {
            'username': 'user',
            'password' : self.password
        }        
        response = self.client.post(self.url, data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_non_existent_user(self):
        data = {
            'username': 'user',
            'password' : 234
        }        
        response = self.client.post(self.url, data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        


class LogOutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="romman",
            password="NewPassword@123"
        )

        # self.token = Token.objects.create(user=self.user)
        self.token = Token.objects.get(user=self.user)
        self.url = reverse("logout")
        
    
    def test_successful_logout(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_logout_without_authentication(self):
        
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    