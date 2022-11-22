from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class PapelNaUSP(models.Model):
    papel = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.papel}'

class Unidade(models.Model):
    unidade = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.unidade}'

class Organizacao(models.Model):
    org = models.CharField(max_length=60)

    def __str__(self):
            return f'{self.org}'

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    cpf = models.CharField(_('CPF'), max_length=11, unique=True)

class Publico(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )

    papel_na_usp = models.ForeignKey(
            PapelNaUSP,
            on_delete=models.CASCADE,
        )

    unidade = models.ForeignKey(
            Unidade,
            on_delete=models.CASCADE,
        )
    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Promotor(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )

    organizacao = models.ForeignKey(
            Organizacao,
            on_delete=models.CASCADE,
        )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

