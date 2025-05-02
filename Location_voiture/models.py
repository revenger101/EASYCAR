# Location_voiture/models.py
from django.db import models

class Admin(models.Model):
    pass

class Client(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class Promoteur(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class Compte(models.Model):
    login = models.CharField(max_length=255)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class Loueur(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class Vehicule(models.Model):
    loueur = models.ForeignKey(Loueur, on_delete=models.CASCADE)
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE, related_name='vehicules_in_agence')
    model = models.CharField(max_length=100)  

    def __str__(self):
        return self.model

class Avis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

class Agence(models.Model):
    promoteur = models.ForeignKey(Promoteur, on_delete=models.CASCADE)
    vehicule = models.ManyToManyField(Vehicule, related_name='agences_with_vehicule')
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class Paiement(models.Model):
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)

    def __str__(self):
        return f"Paiement for {self.agence}"

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Reservation by {self.client} for {self.vehicule}"

class Location(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)

    def __str__(self):
        return f"Location with {self.paiement}"