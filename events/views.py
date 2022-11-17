from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .temp_data import event_data
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from .models import Event, Review, List, Provider
from .forms import EventForm, ReviewForm, ProviderForm

from django.views import generic

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class EventListView(generic.ListView):
    model = Event
    template_name = 'events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed' in self.request.session:
            context['last_movies'] = []
            for event_id in self.request.session['last_viewed']:
                context['last_movies'].append(
                    get_object_or_404(Event, pk=event_id))
        return context

class ListListView(generic.ListView):
    model = List
    template_name = 'events/lists.html'

class ListCreateView(LoginRequiredMixin, PermissionRequiredMixin, 
                        generic.CreateView):
    model = List
    template_name = 'events/create_list.html'
    fields = ['name', 'author', 'events']
    success_url = reverse_lazy('events:lists')

def detail_movie(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if 'last_viewed' not in request.session:
        request.session['last_viewed'] = []
    request.session['last_viewed'] = [event_id] + request.session['last_viewed']
    if len(request.session['last_viewed']) > 5:
        request.session['last_viewed'] = request.session['last_viewed'][:-1]
    context = {'event': event}
    return render(request, 'events/detail.html', context)

def search_movies(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        event_list = Event.objects.filter(name__icontains=search_term)
        context = {"event_list": event_list}
    return render(request, 'events/search.html', context)

@login_required
@permission_required('events.add_movie')
def create_movie(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        provider_form = ProviderForm(request.POST)
        if event_form.is_valid():
            event = Event(**event_form.cleaned_data)
            event.save()
            if provider_form.is_valid(
            ) and provider_form.cleaned_data['service']:
                provider = Provider(event=event, **provider_form.cleaned_data)
                provider.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event.pk, )))
    else:
        event_form = EventForm()
        provider_form = ProviderForm()
    context = {'event_form': event_form, 'provider_form': provider_form}
    return render(request, 'events/create.html', context)

def update_movie(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event.name = form.cleaned_data['name']
            event.release_year = form.cleaned_data['release_year']
            event.poster_url = form.cleaned_data['poster_url']
            event.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event.id, )))
    else:
        form = EventForm(
            initial={
                'name': event.name,
                'release_year': event.release_year,
                'poster_url': event.poster_url
            })

    context = {'event': event, 'form': form}
    return render(request, 'events/update.html', context)


def delete_movie(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event.delete()
        return HttpResponseRedirect(reverse('events:index'))

    context = {'event': event}
    return render(request, 'events/delete.html', context)

def create_review(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_author = request.user
            review_text = form.cleaned_data['text']
            review = Review(author=review_author,
                            text=review_text,
                            event=event)
            review.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event_id, )))
    else:
        form = ReviewForm()
    context = {'form': form, 'event': event}
    return render(request, 'events/review.html', context)

