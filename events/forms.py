from django import forms
from django.forms import ModelForm
from .models import Event, Comment, Formato, Tema, TipoOrganizacao
from accounts.models import Promotor


class EventForm(ModelForm):
    formato = forms.ModelChoiceField(
                    queryset=Formato.objects.all(),
                    required=True, label='Formato',
                )
    
    tema = forms.ModelChoiceField(
                    queryset=Tema.objects.all(),
                    required=True, label='Tema',
                )
    
    tipo_organizacao = forms.ModelChoiceField(
                    queryset=TipoOrganizacao.objects.all(),
                    required=True, label='Tipo de Organização',
                )
    
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
            'date': forms.DateInput(format='%d-%m-%Y'),
            'time': forms.TimeInput(format='%H:%M'),
            'duration': forms.TimeInput(format='%H:%M'),
        }

        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        labels = {
            'text': 'Comentário',
        }