from django.db import models

from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True, default=None)

    title = models.CharField(max_length=100)
    content = models.TextField()

    image = ProcessedImageField(upload_to='post_images',
                                processors=[ResizeToFill(850, 800)],
                                format='JPEG',
                                options={'quality': 90},
                                null=True)
    thumbnail = ImageSpecField(source='image', 
                               processors=[ResizeToFill(350, 250)],
                               format='WEBP', 
                               options={'quality': 60})

    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-created_at']


    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # поле post відносится до Post моделі(related_name='comments') приклад: .prefetch_related('comments__post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # поле author відносится до User моделі(related_name='comments') приклад: .prefetch_related('comments__author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # recursive comment reply system
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    like = models.ManyToManyField(User, related_name='like_comments', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike_comments', blank=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.content
