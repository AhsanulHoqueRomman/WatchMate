from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='WatchListAV'),
    path('list/<int:pk>/', views.WatchDetailsAV.as_view(), name='WatchDetailsAV'),
    
    path('stream/', views.StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>', views.StreamPlatformDetailAV.as_view() , name='streamDetails'),
    
    # path('reviews/', views.ReviewList.as_view(), name='ReviewList'),
    # path('reviews/<int:pk>', views.ReviewDetails.as_view(), name='ReviewDetails'),
    
    path('stream/<int:pk>/review', views.ReviewList.as_view(), name='ReviewList'),
    path('stream/reviews/<int:pk>', views.ReviewDetails.as_view(), name='ReviewDetails'),
]