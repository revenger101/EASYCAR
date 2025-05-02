# Location_voiture/admin.py
from django.contrib import admin
from .models import Client, Vehicule, Agence, Reservation, Location, Paiement, Loueur, Promoteur

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'vehicule', 'agence', 'location')  # Fields to display in the list view

admin.site.register(Client)
admin.site.register(Vehicule)
admin.site.register(Agence)
admin.site.register(Location)
admin.site.register(Paiement)
admin.site.register(Loueur)
admin.site.register(Promoteur)