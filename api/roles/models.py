from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('writer', 'Writer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='writer')

    def __str__(self):
        return self.username
    
class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('pending_review','Pending Review'),
        ('published','Published')
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='draft')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title    