from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .temp_data import event_data
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from .models import Event, Comment, List
from accounts.models import Promotor
from .forms import EventForm, CommentForm

from django.views import generic
import datetime
from django.db.models import Count

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class EventListView(LoginRequiredMixin, generic.ListView):
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

class ListListView(LoginRequiredMixin,generic.ListView):
    model = List
    template_name = 'events/lists.html'

@login_required
def list_events(request):
    event_list = Event.objects.filter(promotor=request.user.id)

    favorite_events = request.user.favorito.all()

    context = {'event_list': event_list, 'favorite_events': favorite_events}
    return render(request, 'events/lists.html', context)

class ListCreateView(LoginRequiredMixin, PermissionRequiredMixin, 
                        generic.CreateView):
    model = List
    template_name = 'events/create_list.html'
    fields = ['name', 'date', 'events']
    success_url = reverse_lazy('events:lists')

@login_required
def detail_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    is_favorite = False
    if event.favorito.filter(id=request.user.id).exists():
        is_favorite = True

    if 'last_viewed' not in request.session:
        request.session['last_viewed'] = []
    request.session['last_viewed'] = [event_id] + request.session['last_viewed']
    if len(request.session['last_viewed']) > 5:
        request.session['last_viewed'] = request.session['last_viewed'][:-1]
    context = {'event': event, 'is_favorite': is_favorite}

    return render(request, 'events/detail.html', context)

@login_required
def favorite_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.favorito.filter(id=request.user.id).exists():
        event.favorito.remove(request.user)

    else:
        event.favorito.add(request.user)

    return HttpResponseRedirect(reverse('events:detail', args=(event.pk, )))

@login_required
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
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = Event(**event_form.cleaned_data)
            event.promotor = Promotor.objects.get(pk=request.user.id)
            event.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event.pk, )))
    else:
        event_form = EventForm()
    context = {'event_form': event_form}
    return render(request, 'events/create.html', context)

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event.name = form.cleaned_data['name']
            event.date = form.cleaned_data['date']
            event.time = form.cleaned_data['time']
            event.duration = form.cleaned_data['duration']
            event.place = form.cleaned_data['place']
            event.description = form.cleaned_data['description']
            event.summary = form.cleaned_data['summary']
            event.max_participants = form.cleaned_data['max_participants']
            event.event_photo_url = form.cleaned_data['event_photo_url']
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
                'max_participants': event.max_participants,
                'event_photo_url': event.event_photo_url
            })

    context = {'event': event, 'form': form}
    return render(request, 'events/update.html', context)

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event.delete()
        return HttpResponseRedirect(reverse('events:index'))

    context = {'event': event}
    return render(request, 'events/delete.html', context)

@login_required
def create_comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_author = request.user
            comment_text = form.cleaned_data['text']
            comment = Comment(author=comment_author,
                            text=comment_text,
                            event=event)
            comment.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event_id, )))
    else:
        form = CommentForm()
    context = {'form': form, 'event': event}
    return render(request, 'events/comment.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    event_list = Event.objects.all().order_by('-date')
    
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')

        event_list.update(approved=False)

        for x in id_list:
            Event.objects.filter(pk=int(x)).update(approved=True)

        return HttpResponseRedirect(reverse('events:admin_approval'))
    
    else:
        return render(request, 'events/admin_approval.html', {"event_list":event_list})

