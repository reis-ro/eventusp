from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PublicoRegisterForm, PromotorRegisterForm
from django.contrib.auth.models import Group 
from django.contrib.auth import login
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from .models import User, Promotor
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


def signup_publico(request):
    if request.method == 'POST':
        form = PublicoRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()                                
            user_group = Group.objects.get(name='publico') 
            user.groups.add(user_group)     

            #login(request, user)                  

            return HttpResponseRedirect(reverse('login'))
    else:
        form = PublicoRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/signup_publico.html', context)

def signup_promotor(request):
    if request.method == 'POST':
        form = PromotorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()                                
            user_group = Group.objects.get(name='promotor_pendente') 
            user.groups.add(user_group)                       

            return HttpResponseRedirect(reverse('login'))
    else:
        form = PromotorRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/signup_promotor.html', context)

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'eventusp3304@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@user_passes_test(lambda u: u.is_superuser)
def admin_approved(request):
    promotor_list = Promotor.objects.filter(approved=True).order_by('-request_date')
    
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')

        for promotor in promotor_list:
            x = promotor.pk
            User.objects.get(pk=int(x)).groups.add(Group.objects.get(name='promotor_pendente'))  
            User.objects.get(pk=int(x)).groups.remove(Group.objects.get(name='promotor')) 

        promotor_list.update(approved=False)

        for x in id_list:
            Promotor.objects.filter(pk=int(x)).update(approved=True)                        
            User.objects.get(pk=int(x)).groups.add(Group.objects.get(name='promotor'))  
            User.objects.get(pk=int(x)).groups.remove(Group.objects.get(name='promotor_pendente'))  
            
        return HttpResponseRedirect(reverse('admin_approved'))
    
    else:
        return render(request, 'accounts/admin_approved.html', {"promotor_list":promotor_list})
    
@user_passes_test(lambda u: u.is_superuser)
def admin_approval(request):
    promotor_list = Promotor.objects.filter(approved=False).order_by('-request_date')
    
    if request.method == "POST":
        id_list = request.POST.getlist('boxes') 
        promotor_list.update(approved=False)

        for x in id_list:
            Promotor.objects.filter(pk=int(x)).update(approved=True)                        
            User.objects.get(pk=int(x)).groups.add(Group.objects.get(name='promotor'))  
            User.objects.get(pk=int(x)).groups.remove(Group.objects.get(name='promotor_pendente'))  
            #print(Promotor.objects.filter(pk=int(x)))
            
        return HttpResponseRedirect(reverse('admin_approval'))
    
    else:
        return render(request, 'accounts/admin_approval.html', {"promotor_list":promotor_list})