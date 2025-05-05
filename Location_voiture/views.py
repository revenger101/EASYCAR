from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import AllocationForm, ClientForm, VehiculeForm, AgenceForm, ContactForm
from .models import Reservation, Location, Paiement, Client, Vehicule, Agence, ContactMessage
from django.contrib import messages

def allocate_vehicle(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            vehicule = form.cleaned_data['vehicule']
            agence = form.cleaned_data['agence']

            # Check if the vehicle is already reserved (has a reservation with a non-null location)
            if Reservation.objects.filter(vehicule=vehicule, location__isnull=False).exists():
                messages.error(request, "Vehicle is already reserved.")
                return render(request, 'allocation.html', {'form': form})

            # Create payment, location, and reservation
            paiement = Paiement.objects.create(agence=agence)
            location = Location.objects.create(paiement=paiement)
            reservation = Reservation.objects.create(
                client=client,
                vehicule=vehicule,
                agence=agence,
                location=location
            )
            messages.success(request, "Vehicle allocated successfully!")
            return redirect('list_allocations')
    else:
        form = AllocationForm()
    return render(request, 'allocation.html', {'form': form})

def list_allocations(request):
    allocations = Reservation.objects.all()
    return render(request, 'allocations_list.html', {'allocations': allocations})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

def add_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_vehicules')
    else:
        form = VehiculeForm()
    return render(request, 'add_vehicule.html', {'form': form})

def add_agence(request):
    if request.method == 'POST':
        form = AgenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_agences')
    else:
        form = AgenceForm()
    return render(request, 'add_agence.html', {'form': form})

def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'list_clients.html', {'clients': clients})

def list_vehicules(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'list_vehicules.html', {'vehicules': vehicules})

def list_agences(request):
    agences = Agence.objects.all()
    return render(request, 'list_agences.html', {'agences': agences})

def home(request):
    return render(request, 'home.html', {
        'title': 'Home Page',
        'message': 'Welcome to the Vehicle Rental System!'
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm()  # Reset form after submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})