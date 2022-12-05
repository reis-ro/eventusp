from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event
from django.db.models import Count


def index(request):
    context = {}
    context['like_count'] = Event.objects.filter(approved = True).annotate(like_count = Count('favorito')).order_by('-like_count')
    return render(request, 'staticpages/index.html', context)


def about(request):
    context = {}
    return render(request, 'staticpages/about.html', context)

# @login_required
# def index_log(request):
#     context = {}
#     return render(request, 'staticpages/index_log.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    context = {}
    return render(request, 'staticpages/approvals.html', context)

def termos(request):
    context = {}
    return render(request, 'staticpages/termos.html', context)

def termos_promotor(request):
    context = {}
    return render(request, 'staticpages/termos_promotor.html', context)