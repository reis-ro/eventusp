from django.forms import ModelForm
from .models import Event, Review, Provider


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'release_year',
            'poster_url',
        ]
        labels = {
            'name': 'Título',
            'release_year': 'Data de Lançamento',
            'poster_url': 'URL do Poster',
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

class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        fields = [
            'service',
            'has_flat_price',
            'price',
        ]
        labels = {
            'service': 'Serviço de Streaming',
            'has_flat_price': 'FLAT?',
            'price': 'Preço',
        } 