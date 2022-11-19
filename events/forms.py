from django import forms
from django.forms import ModelForm
from .models import Event, Review


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'date',
            'time',
            'duration',
            'place',
            'description',
            'summary', 
            'max_participants',
            'cover_photo_url',
            'event_photo_url',
        ]
        labels = {
            'name': 'Nome do evento',
            'date': 'Data',
            'time': 'Hora',
            'duration': 'Duração',
            'place': 'Local',
            'description': 'Descrição do evento',
            'summary': 'Resumo do evento', 
            'max_participants': 'Número máximo de participantes',
            'cover_photo_url': 'Link da foto de capa',
            'event_photo_url': 'Link da foto do evento',
        }
        widget = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date',}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time',}),
            'duration': forms.TimeInput(format='%H:%M', attrs={'type': 'time',}),
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'text',
        ]
        labels = {
            'text': 'Resenha',
        }