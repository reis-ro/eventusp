from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import Group 


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                                
            user_group = Group.objects.get(name='basic_user') 
            user.groups.add(user_group)                       

            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)