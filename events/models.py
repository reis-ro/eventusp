from django.db import models
from django.conf import settings
from accounts.models import Promotor, User

class Formato(models.Model):
    formato = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.formato}'

class Tema(models.Model):
    tema = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.tema}'

class TipoOrganizacao(models.Model):
    tipo_org = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.tipo_org}'

class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('data', null=True, blank=True)
    time = models.TimeField('tempo', null=True, blank=True)
    duration = models.TimeField('duracao', null=True, blank=True)
    place = models.CharField(max_length=50)
    description = models.TextField(max_length=1500)
    summary = models.TextField(max_length=500)
    max_participants = models.IntegerField()
    event_photo_url = models.URLField(max_length=200, null=True)
    approved = models.BooleanField('Aprovado', default=True)
    
    formato = models.ForeignKey(
            Formato,
            on_delete=models.CASCADE,
        )
    
    tema = models.ForeignKey(
            Tema,
            on_delete=models.CASCADE,
        )
    
    tipo_organizacao = models.ForeignKey(
            TipoOrganizacao,
            on_delete=models.CASCADE,
        )

    promotor = models.ForeignKey(
            Promotor,
            on_delete=models.CASCADE,
        )

    favorito = models.ManyToManyField(User, related_name='favorito', blank=True)

    def __str__(self):
        return f'{self.name} ({self.date})'


class Comment(models.Model):
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