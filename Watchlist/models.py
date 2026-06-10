from django.db import models

# Create your models here.



class StreamPlatform(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)
    
    
    def __str__(self):
        return self.name
    



class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    is_released = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    