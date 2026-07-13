from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from Watchlist.api.views import StreamPlatformVS

router = DefaultRouter()
router.register('stream', StreamPlatformVS , basename='stream' )

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='WatchListAV'),
    path('list/<int:pk>/', views.WatchDetailsAV.as_view(), name='WatchDetailsAV'),
    
    #APIView class Urls:
    # path('stream/', views.StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>', views.StreamPlatformDetailAV.as_view() , name='streamDetails'),
    
    #VS router urls:
    path('', include(router.urls)),
    
    # path('reviews/', views.ReviewList.as_view(), name='ReviewList'),
    # path('reviews/<int:pk>', views.ReviewDetails.as_view(), name='ReviewDetails'),
    
    # path('stream/<int:pk>/review_create', views.ReviewCreate.as_view(), name='ReviewCreate'),
    path('<int:pk>/reviews/', views.ReviewListCreate.as_view(), name='ReviewListCreate'),
    path('reviews/<int:pk>/', views.ReviewDetails.as_view(), name='ReviewDetails'),
    
]