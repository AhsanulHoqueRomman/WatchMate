from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Watchlist.models import StreamPlatform
from Watchlist import models
from Watchlist.api.serializers import StreamPlatformSerializer


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
            self.user = User.objects.create_user(username='romman', password='password123')
            self.token = Token.objects.get(user__username = self.user)
            self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + self.token.key)
            
            self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = 'No 1 stream platform',website ='https://netflix.com')
        
    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about' : 'No 1 stream platform',
            'website' : 'https://netflix.com'
        }
        
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_indv(self):
        response = self.client.get(reverse('stream-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)