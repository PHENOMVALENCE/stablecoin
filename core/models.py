from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    )
    LANGUAGES = (
        ('en', 'English'),
        ('sw', 'Swahili'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    language = models.CharField(max_length=2, choices=Post.LANGUAGES)

    def __str__(self):
        return self.question


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    flyer = models.ImageField(upload_to='event_flyers/', blank=True, null=True)
    design = RichTextField(blank=True)
    show = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"
