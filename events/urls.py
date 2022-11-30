from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),  # edite esta linha
    path('search/', views.search_events, name='search'),
    path('create/', views.create_event, name='create'),
    path('<int:event_id>/', views.detail_event,
         name='detail'), 
    path('update/<int:event_id>/', views.update_event, name='update'),
    path('delete/<int:event_id>/', views.delete_event, name='delete'),
    path('<int:event_id>/comment/', views.create_comment, name='comment'),
    path('lists/', views.ListListView.as_view(), name='lists'),
    path('lists/create', views.ListCreateView.as_view(), name='create-list'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
]