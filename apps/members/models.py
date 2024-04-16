from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(null=True, blank=True)
    avatar = ProcessedImageField(
        upload_to='avatars',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        blank=True
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 50}
    )

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(self.user.username)


    def get_avatar_thumbnail(self):
        if self.avatar_thumbnail:
            return self.avatar_thumbnail.url
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(self.user.username)
