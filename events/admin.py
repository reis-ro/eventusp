from django.contrib import admin

from .models import Event, Review, List, Provider

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(List)
admin.site.register(Provider) 