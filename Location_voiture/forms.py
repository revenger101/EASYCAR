# Location_voiture/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Client, Vehicule, Agence, Promoteur

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name']

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['client', 'agence', 'model', 'picture', 'price', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.1'}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }
        labels = {
            'client': 'Vehicle Owner',
            'agence': 'Agency',
            'model': 'Vehicle Model',
            'picture': 'Vehicle Picture',
            'price': 'Daily Price ($)',
            'rating': 'Vehicle Rating (0-5)',
        }

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['promoteur', 'name', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.1'}),
        }

class AllocationForm(forms.Form):
    vehicule = forms.ModelChoiceField(queryset=Vehicule.objects.all(), label='Select Vehicle')
    agence = forms.ModelChoiceField(queryset=Agence.objects.all(), label='Select Agency')
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date'
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Date'
    )

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}), required=True)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Create a Client record for this user
            Client.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}"
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['profile_picture', 'phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'profile_picture': 'Profile Picture',
            'phone': 'Phone Number',
            'address': 'Address',
            'date_of_birth': 'Date of Birth',
        }

class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('attijari', 'Attijari Bank'),
        ('paypal', 'PayPal'),
        ('biat', 'BIAT (Banque Internationale Arabe de Tunisie)'),
        ('stb', 'STB (Société Tunisienne de Banque)'),
        ('amen_bank', 'Amen Bank'),
        ('credit_card', 'Credit/Debit Card'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'}),
        label='Select Payment Method'
    )

    # Credit Card Fields
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'data-payment-method': 'credit_card'
        }),
        label='Card Number'
    )

    card_holder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'John Doe',
            'data-payment-method': 'credit_card'
        }),
        label='Card Holder Name'
    )

    expiry_date = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'data-payment-method': 'credit_card'
        }),
        label='Expiry Date'
    )

    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'data-payment-method': 'credit_card'
        }),
        label='CVV'
    )

    # Bank Account Fields
    account_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Account Number',
            'data-payment-method': 'bank'
        }),
        label='Account Number'
    )

    # PayPal Fields
    paypal_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your-email@example.com',
            'data-payment-method': 'paypal'
        }),
        label='PayPal Email'
    )