from django.db import models

from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True, default=None)

    title = models.CharField(max_length=100)
    content = RichTextField('Text', config_name='extends')

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

    tags = models.ManyToManyField('Tag', related_name='tags', null=True, blank=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self) -> str:
        return self.title


    def get_post_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png?20200912122019'


    def get_post_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png?20200912122019'


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



class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
