from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from Watchlist.models import WatchList, StreamPlatform, Review
from Watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from Watchlist.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly


#Below are the FUNCTION BASED VIEWS:

'''

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request,pk):
    try:
        movie = Movie.objects.get( pk=pk)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)    
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
'''



class WatchListAV(APIView):
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WatchDetailsAV(APIView):
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get( pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put (self, request, pk):
        try:
            movie = WatchList.objects.get( pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get( pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#Using APIView:

'''

class StreamPlatformAV(APIView):
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,  many=True)     #To use the HyperlinkedRelatedField we have to pass 'context ={''request':request}'
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamPlatformDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get( pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get( pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,  data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, pk):
        try:
            platform = StreamPlatform.objects.get( pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''


#Using Mixins

'''
  
class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    

class ReviewDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
        
'''


#Usinng Concrete view classes - Gnereic APIView classes

class ReviewListCreate(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        
        reviewer = self.request.user
        reviewer_queryset = Review.objects.filter(watchlist = watchlist, reviewer=reviewer)
        if reviewer_queryset.exists():
            raise ValidationError("You have already reviewd this content!")
        
        # if watchlist.number_of_reviews == 0:
        #     watchlist.avg_rating = serializer.validate_data['rating']
        # else:
        #     watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) /2
            
        # watchlist.number_of_reviews = watchlist.number_of_reviews + 1
        # watchlist.save()
        
        #Another way to count the Average rating of watchlist:
        
        ## Get the new rating from validated data:
        rating = serializer.validated_data['rating']
        # Calculate total rating before adding new review:
        total_rating =(watchlist.avg_rating * watchlist.number_of_reviews)
        # Update review count:
        watchlist.number_of_reviews = watchlist.number_of_reviews + 1
        # Calculate new average rating:
        watchlist.avg_rating = (total_rating + rating ) / watchlist.number_of_reviews
        watchlist.save()
    
        serializer.save(watchlist=watchlist, reviewer=reviewer)
    
# class ReviewCreate(generics.CreateAPIView):
#     serializer_class = ReviewSerializer
    
#     def perform_create(self, serializer):
#         pk = self.kwargs['pk']
#         watchlist = WatchList.objects.get(pk=pk)
#         serializer.save(watchlist=watchlist)
    
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]



#Using viewsets.ViewSet class- We have to manually write individual function to list,create,post,update,delete.

'''

class StreamPlatformVS(viewsets.ViewSet):
    def list(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get( pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,  data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get( pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
'''


# Using ModelViewSet -We don't have to write all the fucntions like ViewSet class. we just have to write the queryset and the serializer class.

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    
    
#  There is another class named ReadOnlyModelViewSet which is used for Read Only uses in full element list or individual list.

'''
class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

'''

