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