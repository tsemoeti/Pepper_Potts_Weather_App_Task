from django.db import models

class WeatherData(models.Model):
    city_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city_name