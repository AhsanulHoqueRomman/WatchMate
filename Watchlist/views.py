from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse

# Create your views here.

def movie_list(request):
    movies = Movie.objects.all()
    context = {
        'movies' : list(movies)
    }
    return JsonResponse(context)

def movie_details(request,pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'name' : movie.name,
        'description' : movie.description,
        'active' : movie.active,
    }
    
    return JsonResponse(context)