from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Watchlist.models import StreamPlatform, WatchList
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
        
        
        
class WatchlistTestCase(APITestCase):
    
    def setUp(self):
        
        self.url = reverse('WatchListAV')
         
        self.platform = StreamPlatform.objects.create(name = 'Netflix', about = 'No 1 stream platform',website ='https://netflix.com')
        self.valid_data = {
            "title": "Interstellar",
            "description": "A science fiction movie",
            "platform": self.platform.id,
            "is_released": True,
            "avg_rating": 4.5,
            "number_of_reviews": 10
        }
        
    def test_get_watchlist(self):
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    def test_create_watchlist(self):

        response = self.client.post(self.url,self.valid_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(WatchList.objects.count(),1)
        self.assertEqual(models.WatchList.objects.get().title,"Interstellar" )
         
    def test_create_watchlist_without_title(self):

        data = self.valid_data.copy()
        data.pop("title")
        
        response = self.client.post(self.url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        
    def test_create_watchlist_invalid_platform(self):

        data = self.valid_data.copy()
        data["platform"] = 9999

        response = self.client.post(self.url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("platform",response.data)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                description="Example Movie", is_released=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                description="Example Movie", is_released=True)
        self.review = models.Review.objects.create(reviewer=self.user, rating=5, review="Great Movie", 
                                watchlist=self.watchlist2, active=True)
    
    def test_review_create(self):
        data = {
            "reviewer": self.user,
            "rating": 5,
            "review": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('ReviewListCreate', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(reverse('ReviewListCreate', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "reviewer": self.user,
            "rating": 5,
            "review": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('ReviewListCreate', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "reviewer": self.user,
            "rating": 4,
            "review": "Great Movie! - Updated",
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('ReviewDetails', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('ReviewListCreate', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_ind(self):
        response = self.client.get(reverse('ReviewDetails', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind_delete(self):
        response = self.client.delete(reverse('ReviewDetails', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)