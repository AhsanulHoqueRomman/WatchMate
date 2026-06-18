from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from Watchlist.api.views import StreamPlatform

router = DefaultRouter()
router.register('stream', StreamPlatform , basename='stream' )

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='WatchListAV'),
    path('list/<int:pk>/', views.WatchDetailsAV.as_view(), name='WatchDetailsAV'),
    
    #APIView class Urls:
    # path('stream/', views.StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>', views.StreamPlatformDetailAV.as_view() , name='streamDetails'),
    
    # path('reviews/', views.ReviewList.as_view(), name='ReviewList'),
    # path('reviews/<int:pk>', views.ReviewDetails.as_view(), name='ReviewDetails'),
    
    # path('stream/<int:pk>/review_create', views.ReviewCreate.as_view(), name='ReviewCreate'),
    path('stream/<int:pk>/review', views.ReviewListCreate.as_view(), name='ReviewListCreate'),
    path('stream/reviews/<int:pk>', views.ReviewDetails.as_view(), name='ReviewDetails'),
    path('', include(router.urls))
]