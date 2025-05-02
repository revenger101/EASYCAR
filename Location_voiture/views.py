from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AllocationForm , ClientForm, VehiculeForm, AgenceForm
from .models import Reservation, Location, Paiement , Client , Vehicule , Agence

def allocate_vehicle(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            vehicule = form.cleaned_data['vehicule']
            agence = form.cleaned_data['agence']

            if not Reservation.objects.filter(vehicule=vehicule, location__isnull=True).exists():
                return HttpResponse("Vehicle is already reserved.")

            paiement = Paiement.objects.create(agence=agence)
            location = Location.objects.create(paiement=paiement)
            reservation = Reservation.objects.create(
                client=client,
                vehicule=vehicule,
                agence=agence,
                location=location
            )
            return HttpResponse("Vehicle allocated successfully!")
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