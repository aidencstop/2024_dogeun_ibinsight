from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category

    def __str__(self):
        return self.name


class Hashtags(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the hashtag

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)  # Title of the post
    content = models.TextField()  # Main content of the post
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # User who created the post (can be null)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)  # Many-to-many relationship with categories
    hashtags = models.ManyToManyField(Hashtags, related_name='posts', blank=True)  # Many-to-many relationship with hashtags

    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Link to the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # User who made the comment
    text = models.TextField()  # Comment content
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
