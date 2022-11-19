from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('data', null=True, blank=True)
    time = models.TimeField('tempo', null=True, blank=True)
    duration = models.TimeField('tempo', null=True, blank=True)
    place = models.CharField(max_length=50)
    description = models.CharField(max_length=1500)
    summary = models.CharField(max_length=500)
    max_participants = models.IntegerField()
    cover_photo_url = models.URLField(max_length=200, null=True)
    event_photo_url = models.URLField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name} ({self.date})'


class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.text}" - {self.author.username}'
        
class List(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return f'{self.name} by {self.author}'