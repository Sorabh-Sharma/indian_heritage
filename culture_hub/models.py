from django.db import models
from django.contrib.auth.models import User

class HeritageItem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='heritage_items')
    title = models.CharField(max_length=200)      # e.g., "Taj Mahal" or "Diwali"
    category = models.CharField(max_length=100)   # e.g., "Monument" or "Festival"
    region = models.CharField(max_length=100)     # e.g., "Uttar Pradesh" or "All India"
    description = models.TextField()              # A longer paragraph describing it
    latitude = models.FloatField(null=True, blank=True)   # GPS latitude for map pin
    longitude = models.FloatField(null=True, blank=True)  # GPS longitude for map pin

    def __str__(self):
        return self.title
