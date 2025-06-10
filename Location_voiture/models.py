# Location_voiture/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Admin(models.Model):
    pass

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, help_text="Vehicle owner/client")
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE, related_name='vehicules_in_agence')
    model = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        help_text="Rating from 0.0 to 5.0"
    )

    def __str__(self):
        return self.model

class Avis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

class Agence(models.Model):
    promoteur = models.ForeignKey(Promoteur, on_delete=models.CASCADE)
    vehicule = models.ManyToManyField(Vehicule, related_name='agences_with_vehicule')
    name = models.CharField(max_length=100)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        help_text="Agency rating from 0.0 to 5.0"
    )

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
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
        ('refunded', 'Refunded'),
    ]

    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)
    date_debut = models.DateField(null=True, blank=True, help_text="Start date of the rental")
    date_fin = models.DateField(null=True, blank=True, help_text="End date of the rental")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, help_text="Total amount in DT")
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Location with {self.paiement} - {self.payment_status}"

    def calculate_total_amount(self, vehicule):
        """Calculate total amount based on rental duration and vehicle price"""
        if self.date_debut and self.date_fin and vehicule:
            days = (self.date_fin - self.date_debut).days + 1
            return float(vehicule.price) * days
        return 0.0
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"