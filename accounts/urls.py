from django.urls import path
from accounts.views import LoginView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/publico/', views.signup_publico, name='signup'),
    path('signup/promotor/', views.signup_promotor, name='signup_promotor'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),   
    path("reset/password_reset", views.password_reset_request, name="reset/password_reset"),
    path('admin_approval', views.admin_approval, name='admin_approval'), 
    path('admin_approved', views.admin_approved, name='admin_approved'), 
]