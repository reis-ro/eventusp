from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),  # edite esta linha
    path('search/', views.search_movies, name='search'),
    path('create/', views.create_movie, name='create'),
    path('<int:event_id>/', views.detail_movie,
         name='detail'), 
    path('update/<int:event_id>/', views.update_movie, name='update'),
    path('delete/<int:event_id>/', views.delete_movie, name='delete'),
    path('<int:event_id>/review/', views.create_review, name='review'),
    path('lists/', views.ListListView.as_view(), name='lists'),
    path('lists/create', views.ListCreateView.as_view(), name='create-list'),
]