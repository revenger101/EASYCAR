# Location_voiture/forms.py
from django import forms
from .models import Client, Vehicule, Agence, Loueur, Promoteur

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name']

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['loueur', 'agence', 'model']

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['promoteur', 'name']

class AllocationForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    vehicule = forms.ModelChoiceField(queryset=Vehicule.objects.all())
    agence = forms.ModelChoiceField(queryset=Agence.objects.all())

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}), required=True)