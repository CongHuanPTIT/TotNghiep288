from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


# Create your models here.
class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    # If the user is deleted, all videos uploaded by this user will also be deleted
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='uploads/video_files',
                                  validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])])
    thumbnail = models.FileField(upload_to='uploads/thumbnails',
                                 validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    date_posted = models.DateTimeField(default=timezone.now)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL)


class Topic(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.name, self.description)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.user} | Created on {self.created_on.strftime("%b-%d-%Y %I:%M:%p")}'
