from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-post_date']

 
    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')  # Fix: Correct model reference
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Ensure this field exists
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Ensures comments are sorted by latest first

    def __str__(self):
        return f'Comment by {self.author} on {self.blog.title}'  # Fix: Correct reference to blog title
