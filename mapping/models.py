from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Park(models.Model):
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='parks')
    name = models.CharField(max_length=100, help_text="Official name of the park", blank=True)
    description = models.TextField(blank=True,null=True)
    latitude = models.FloatField(help_text="Geographic latitude in decimal degrees")
    longitude = models.FloatField(help_text="Geographic longitude in decimal degrees")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'parks'

    def __str__(self):
        return self.name

class ParkDescription(models.Model):
    park = models.OneToOneField(Park, on_delete= models.CASCADE , primary_key=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True, help_text="Full address of the park")
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='park_images/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Description for {self.name}"


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='submissions')
    place = models.ForeignKey(Park, on_delete=models.CASCADE,related_name='submissions')
    note = models.TextField(help_text="User's comments about the park")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Moderation status"
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'submissions'

    def __str__(self):
        return f"Submission by {self.user.email} for {self.place.name}"