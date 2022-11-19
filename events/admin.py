from django.contrib import admin

from .models import Event, Review, List
from accounts.models import User, Publico, Promotor, PapelNaUSP, Unidade, Organizacao

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(List)
admin.site.register(User)
admin.site.register(Publico)
admin.site.register(Promotor)
admin.site.register(PapelNaUSP)
admin.site.register(Unidade)
admin.site.register(Organizacao)
