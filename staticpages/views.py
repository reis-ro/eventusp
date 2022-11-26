from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


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

@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    context = {}
    return render(request, 'staticpages/approvals.html', context)