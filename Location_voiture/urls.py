from django.urls import path
from . import views

urlpatterns = [
    
    path('home/', views.home, name='home'),
    path('allocate/', views.allocate_vehicle, name='allocate_vehicle'),
    path('allocations/', views.list_allocations, name='list_allocations'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/', views.list_clients, name='list_clients'),
    path('vehicules/add/', views.add_vehicule, name='add_vehicule'),
    path('vehicules/', views.list_vehicules, name='list_vehicules'),
    path('agences/add/', views.add_agence, name='add_agence'),
    path('agences/', views.list_agences, name='list_agences'),  
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
]
