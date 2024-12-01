from django.db import models
from django.contrib.auth.models import User

class WrappedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    top_artists = models.JSONField()
    top_tracks = models.JSONField()
    top_genres = models.JSONField()
    listening_stats = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
