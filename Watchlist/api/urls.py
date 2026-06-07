from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.MovieListAV.as_view(), name='MovieListAV'),
    path('list/<int:pk>/', views.MovieDetailsAV.as_view(), name='MovieDetailsAV'),
]