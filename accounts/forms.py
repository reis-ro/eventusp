from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Publico, Promotor, User, PapelNaUSP, Unidade, Organizacao
from django.db import transaction

class PublicoRegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    #cpf = forms.CharField(max_length=11, required=True)

    papel_na_usp = forms.ModelChoiceField(
                    queryset=PapelNaUSP.objects.all(),
                    required=True
                )

    unidade = forms.ModelChoiceField(
                    queryset=Unidade.objects.all(),
                    required=True
            )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = User(username=self.cleaned_data.get('email'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email=self.cleaned_data.get('email'),
                    cpf=self.cleaned_data.get('cpf')
                    )
        user.save()
        publico = Publico.objects.create(
                        user=user,
                        papel_na_usp=self.cleaned_data.get('papel_na_usp'),
                        unidade=self.cleaned_data.get('unidade')
                        )
        publico.save()
        return publico

class PromotorRegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    cpf = forms.CharField(max_length=11, required=True)

    organizacao = forms.ModelChoiceField(
                    queryset=Organizacao.objects.all(),
                    required=True
                )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        model.username = model.email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        promotor = Promotor.objects.create(user=user)
        #promotor.cpf.add(*self.cleaned_data.get('cpf'))
        promotor.organizacao.add(*self.cleaned_data.get('organizacao'))
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

# class PublicoCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=50) # Required
#     last_name = forms.CharField(max_length=50) # Required

#     class Meta:
#         model = Publico
#         fields = ['username', 
#                 'first_name', 
#                 'last_name', 
#                 'email', 
#                 'cpf',]

#         labels = {'username': 'Nome de Usuário',
#                 'first_name':'Nome', 
#                 'last_name': 'Sobrenome', 
#                 'email': 'Email', 
#                 'cpf': 'CPF',}