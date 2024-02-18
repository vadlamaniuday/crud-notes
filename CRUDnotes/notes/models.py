from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# generate a note model where the author is the specified user
class Note(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_users = models.ManyToManyField(User, related_name="shared_notes")
    published_at = models.DateTimeField(auto_now_add=True)
    versions = models.JSONField(default=list)

    def __str__(self):
        return self.title
