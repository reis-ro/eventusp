from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .temp_data import event_data
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from .models import Event, Review, List
from .forms import EventForm, ReviewForm

from django.views import generic

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class EventListView(generic.ListView):
    model = Event
    template_name = 'events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed' in self.request.session:
            context['last_events'] = []
            for event_id in self.request.session['last_viewed']:
                context['last_events'].append(
                    get_object_or_404(Event, pk=event_id))
        return context

class ListListView(generic.ListView):
    model = List
    template_name = 'events/lists.html'

class ListCreateView(LoginRequiredMixin, PermissionRequiredMixin, 
                        generic.CreateView):
    model = List
    template_name = 'events/create_list.html'
    fields = ['name', 'date', 'events']
    success_url = reverse_lazy('events:lists')

def detail_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if 'last_viewed' not in request.session:
        request.session['last_viewed'] = []
    request.session['last_viewed'] = [event_id] + request.session['last_viewed']
    if len(request.session['last_viewed']) > 5:
        request.session['last_viewed'] = request.session['last_viewed'][:-1]
    context = {'event': event}
    return render(request, 'events/detail.html', context)

def search_events(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        event_list = Event.objects.filter(name__icontains=search_term)
        context = {"event_list": event_list}
    return render(request, 'events/search.html', context)

@login_required
@permission_required('events.add_event')
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = Event(**event_form.cleaned_data)
            event.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event.pk, )))
    else:
        event_form = EventForm()
    context = {'event_form': event_form}
    return render(request, 'events/create.html', context)

def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event.name = form.cleaned_data['name']
            event.date = form.cleaned_data['date']
            event.poster_url = form.cleaned_data['poster_url']
            event.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event.id, )))
    else:
        form = EventForm(
            initial={
                'name': event.name,
                'date': event.date,
                'time': event.time,
                'duration': event.duration,
                'place': event.place,
                'description': event.description,
                'summary': event.summary,
                'max_participants': event.max_paticipants,
                'cover_photo_url': event.cover_photo_url,
                'event_photo_url': event.event_photo_url
            })

    context = {'event': event, 'form': form}
    return render(request, 'events/update.html', context)


def delete_event(request, event_id):
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

@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    event_list = Event.objects.all().order_by('-date')
    return render(request, 'events/admin_approval.html', {"event_list":event_list})

