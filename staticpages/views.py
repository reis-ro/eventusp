from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}
    return render(request, 'staticpages/index.html', context)


def about(request):
    context = {}
    return render(request, 'staticpages/about.html', context)

@login_required
def index_log(request):
    context = {}
    return render(request, 'staticpages/index_log.html', context)