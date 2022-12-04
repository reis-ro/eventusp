from django.contrib import admin

from .models import Event, Comment, List
from accounts.models import User, Publico, Promotor, PapelNaUSP, Unidade, Organizacao
from events.models import Formato, Tema, TipoOrganizacao

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(List)
admin.site.register(User)
admin.site.register(Publico)
admin.site.register(Promotor)
admin.site.register(PapelNaUSP)
admin.site.register(Unidade)
admin.site.register(Organizacao)
admin.site.register(Formato)
admin.site.register(Tema)
admin.site.register(TipoOrganizacao)
