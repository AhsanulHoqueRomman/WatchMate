from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='WatchListAV'),
    path('list/<int:pk>/', views.WatchDetailsAV.as_view(), name='WatchDetailsAV'),
    
    path('platform/', views.StreamPlatformAV.as_view(), name='platform'),
    path('platform/<int:pk>', views.StreamPlatformDetailAV.as_view() , name='platform'),
]