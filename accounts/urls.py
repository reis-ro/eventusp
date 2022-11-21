from django.urls import path
from accounts.views import LoginView

from . import views

urlpatterns = [
    path('signup/publico/', views.signup_publico, name='signup'),
    path('signup/promotor/', views.signup_promotor, name='signup_promotor'),
    path('login/', LoginView.as_view(), name='login'),
]