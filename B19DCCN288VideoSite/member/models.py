from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Member(models.Model):                                      # One member has one profile. If deleted,
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # the profile will be deleted along with the member
    name = models.CharField(max_length=100, blank=False)
    date_of_birth = models.DateField(blank=False)
    other = models.TextField(max_length=1500, blank=True)
    profile_image = models.FileField(upload_to='uploads/profile_images',
                                     validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])

    def __str__(self):
        return f'Welcome, {self.user.username}'
