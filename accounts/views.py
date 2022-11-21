from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PublicoRegisterForm, PromotorRegisterForm
from django.contrib.auth.models import Group 
from django.contrib.auth import login


def signup_publico(request):
    if request.method == 'POST':
        form = PublicoRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()                                
            user_group = Group.objects.get(name='publico') 
            user.groups.add(user_group)     

            login(request, user)                  

            return HttpResponseRedirect(reverse('login'))
    else:
        form = PublicoRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/signup_publico.html', context)

def signup_promotor(request):
    if request.method == 'POST':
        form = PromotorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()                                
            user_group = Group.objects.get(name='promotor') 
            user.groups.add(user_group)                       

            return HttpResponseRedirect(reverse('login'))
    else:
        form = PromotorRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/signup_promotor.html', context)

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'