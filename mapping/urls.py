from django.urls import path
from .views import ParkListCreateAPIView
from . import views

urlpatterns = [
    path('parks/', ParkListCreateAPIView.as_view(), name='park-list-create'),
    path('map/', views.map, name='map'),
    path('navbar/', views.location, name='navbar'),
    path('add-park/', views.add_park, name='add-park'),
    path('delete-park/<int:park_id>/', views.delete_park, name='delete-park'),
    path('edit-park/<int:park_id>/', views.edit_park, name='edit-park'),
    # path('description/<int:park_id>/', views.showDescription, name='parkDecription'),
    path('<int:park_id>/description/', views.park_description, name='park_description'),
    path('<int:park_id>/add-description/', views.create_park_description, name='create_park_description'),

]
