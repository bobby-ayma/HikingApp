from django.contrib import admin
from .models import Hike, Comment, Like

# Register your models here.
admin.site.register(Hike)
admin.site.register(Comment)
admin.site.register(Like)