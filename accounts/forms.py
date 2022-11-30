from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Publico, Promotor, User, PapelNaUSP, Unidade, Organizacao
from django.db import transaction
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

class PublicoRegisterForm(UserCreationForm):
    papel_na_usp = forms.ModelChoiceField(
                    queryset=PapelNaUSP.objects.all(),
                    required=True, label='Papel na USP',
                )

    unidade = forms.ModelChoiceField(
                    queryset=Unidade.objects.all(),
                    required=True
            )
#mark_safe('Li e concordo com os <a href="//www.blogger.com/questions/whyname/" "termos de uso"></a>)')
    # terms_and_conditions = reverse_lazy("login")
    termos_de_uso = forms.BooleanField()
    #termos_de_uso = forms.BooleanField(label = "Privacy <a href='%s' a>policy</a>" % reverse('termos_de_uso'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'password1', 'password2']
        labels = {'first_name': 'Nome', 'last_name': 'Sobrenome', 'email': 'Email', 'cpf': 'CPF'}

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
    organizacao = forms.ModelChoiceField(
                    queryset=Organizacao.objects.all(),
                    required=True,
                    label='Organização'
                )
    
    profile_photo = forms.ImageField(label='Foto de Perfil', required=False)

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

        promotor = Promotor.objects.create(user=user, 
                                organizacao=self.cleaned_data.get('organizacao'))

        promotor.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')