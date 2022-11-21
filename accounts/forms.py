from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Publico, Promotor, User, PapelNaUSP, Unidade, Organizacao
from django.db import transaction
from django.core.exceptions import ValidationError

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

    def clean_cpf(self):

        cpf = self.cleaned_data.get('cpf')

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise ValidationError("CPF Inválido!")

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise ValidationError("CPF Inválido!")

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise ValidationError("CPF Inválido!")

        return cpf


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)

        user.username=self.cleaned_data.get('email')
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.cpf=self.cleaned_data.get('cpf')

        user.save()

        publico = Publico.objects.create(
                        user=user,
                        papel_na_usp=self.cleaned_data.get('papel_na_usp'),
                        unidade=self.cleaned_data.get('unidade')
                        )
        publico.save()

        return user

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