from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.user_login, name='login'),  # Make login the default page
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # Main app URLs (all require login)
    path('home/', views.home, name='home'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('allocate/', views.allocate_vehicle, name='allocate_vehicle'),
    path('allocations/', views.list_allocations, name='list_allocations'),
    path('payment/<int:location_id>/', views.payment_view, name='payment_view'),
    path('reject/<int:location_id>/', views.reject_allocation, name='reject_allocation'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/', views.list_clients, name='list_clients'),
    path('vehicules/add/', views.add_vehicule, name='add_vehicule'),
    path('vehicules/', views.list_vehicules, name='list_vehicules'),
    path('agences/add/', views.add_agence, name='add_agence'),
    path('agences/', views.list_agences, name='list_agences'),
    path('contact/', views.contact, name='contact'),
]
