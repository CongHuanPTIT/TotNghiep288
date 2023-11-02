from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE) # If the user is deleted, all videos uploaded by this
                                                                 # user will also be deleted
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='uploads/video_files',
                                  validators = [FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])])
    thumbnail = models.FileField(upload_to='uploads/thumbnails',
                                 validators = [FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    date_posted = models.DateTimeField(default=timezone.now)