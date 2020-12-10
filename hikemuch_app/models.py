

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Hike(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    image = models.ImageField(
        upload_to='hikes', #to add gps track
    )


    def __str__(self):
        return self.name
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    definition = models.CharField(max_length=2, default=0)


class Comment(models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

