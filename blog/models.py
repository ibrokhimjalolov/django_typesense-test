from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    number = models.IntegerField(default=5)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()

    def __str__(self):
        return self.body
