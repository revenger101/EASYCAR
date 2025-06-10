from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import AllocationForm, ClientForm, VehiculeForm, AgenceForm, ContactForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, ClientProfileForm, PaymentForm
from .models import Reservation, Location, Paiement, Client, Vehicule, Agence, ContactMessage
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

@login_required
def allocate_vehicle(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            # Get the client associated with the logged-in user
            try:
                client = Client.objects.get(user=request.user)
            except Client.DoesNotExist:
                # Create a client if it doesn't exist
                client = Client.objects.create(
                    user=request.user,
                    name=f"{request.user.first_name} {request.user.last_name}"
                )

            vehicule = form.cleaned_data['vehicule']
            agence = form.cleaned_data['agence']
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            # Check if the vehicle is already reserved (has a reservation with a non-null location)
            if Reservation.objects.filter(vehicule=vehicule, location__isnull=False).exists():
                messages.error(request, "Vehicle is already reserved.")
                return render(request, 'allocation.html', {'form': form, 'vehicule': vehicule})

            # Create payment, location, and reservation
            paiement = Paiement.objects.create(agence=agence)
            location = Location.objects.create(
                paiement=paiement,
                date_debut=date_debut,
                date_fin=date_fin,
                payment_status='pending'
            )
            # Calculate total amount
            location.total_amount = location.calculate_total_amount(vehicule)
            location.save()

            reservation = Reservation.objects.create(
                client=client,
                vehicule=vehicule,
                agence=agence,
                location=location
            )
            messages.success(request, f"Vehicle {vehicule.model} allocated successfully from {date_debut} to {date_fin}!")
            return redirect('list_allocations')
    else:
        form = AllocationForm()

    # Get vehicle details if vehicle ID is passed
    selected_vehicule = None
    if 'vehicule_id' in request.GET:
        try:
            selected_vehicule = Vehicule.objects.get(id=request.GET['vehicule_id'])
        except Vehicule.DoesNotExist:
            pass

    return render(request, 'allocation.html', {
        'form': form,
        'selected_vehicule': selected_vehicule,
        'user_name': f"{request.user.first_name} {request.user.last_name}"
    })

@login_required
def list_allocations(request):
    # Show only allocations for the current user
    try:
        client = Client.objects.get(user=request.user)
        allocations = Reservation.objects.filter(client=client)
    except Client.DoesNotExist:
        client = None
        allocations = []
    return render(request, 'allocations_list.html', {
        'allocations': allocations,
        'client': client
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

@login_required
def add_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully!")
            return redirect('list_vehicules')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VehiculeForm()
    return render(request, 'add_vehicule.html', {'form': form})

@login_required
def add_agence(request):
    if request.method == 'POST':
        form = AgenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_agences')
    else:
        form = AgenceForm()
    return render(request, 'add_agence.html', {'form': form})

@login_required
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'list_clients.html', {'clients': clients})

@login_required
def list_vehicules(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'list_vehicules.html', {'vehicules': vehicules})

@login_required
def list_agences(request):
    agences = Agence.objects.all()
    return render(request, 'list_agences.html', {'agences': agences})

def home(request):
    context = {
        'title': 'Home Page',
    }
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)
            context['client'] = client
            context['message'] = f'Welcome to the Vehicle Rental System, {request.user.first_name}!'
        except Client.DoesNotExist:
            context['client'] = None
            context['message'] = f'Welcome to the Vehicle Rental System, {request.user.first_name}!'
    return render(request, 'home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, f"Welcome {user.first_name}! Your account has been created successfully.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    # Render a logout page that clears localStorage and redirects
    return render(request, 'logout.html')

@login_required
def profile_view(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        # Create a client if it doesn't exist
        client = Client.objects.create(
            user=request.user,
            name=f"{request.user.first_name} {request.user.last_name}"
        )

    return render(request, 'profile.html', {
        'client': client,
        'user': request.user
    })

@login_required
def profile_edit(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        # Create a client if it doesn't exist
        client = Client.objects.create(
            user=request.user,
            name=f"{request.user.first_name} {request.user.last_name}"
        )

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        client_form = ClientProfileForm(request.POST, request.FILES, instance=client)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client_instance = client_form.save(commit=False)
            # Update client name when user name changes
            client_instance.name = f"{user.first_name} {user.last_name}"
            client_instance.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile_view')
    else:
        user_form = UserProfileForm(instance=request.user)
        client_form = ClientProfileForm(instance=client)

    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'client_form': client_form,
        'client': client
    })

@login_required
def payment_view(request, location_id):
    try:
        client = Client.objects.get(user=request.user)
        location = Location.objects.get(id=location_id)
        reservation = Reservation.objects.get(location=location, client=client)
    except (Client.DoesNotExist, Location.DoesNotExist, Reservation.DoesNotExist):
        messages.error(request, "Invalid payment request.")
        return redirect('list_allocations')

    if location.payment_status != 'pending':
        messages.info(request, "This booking has already been processed.")
        return redirect('list_allocations')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment based on method
            payment_method = form.cleaned_data['payment_method']

            # Update location with payment details
            location.payment_method = payment_method
            location.payment_status = 'paid'
            location.payment_date = timezone.now()

            # Generate payment reference
            import random
            import string
            location.payment_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            location.save()

            messages.success(request, f"Payment successful! Reference: {location.payment_reference}")
            return redirect('list_allocations')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {
        'form': form,
        'location': location,
        'reservation': reservation,
        'vehicule': reservation.vehicule,
        'total_amount': location.total_amount
    })

@login_required
def reject_allocation(request, location_id):
    try:
        client = Client.objects.get(user=request.user)
        location = Location.objects.get(id=location_id)
        reservation = Reservation.objects.get(location=location, client=client)
    except (Client.DoesNotExist, Location.DoesNotExist, Reservation.DoesNotExist):
        messages.error(request, "Invalid request.")
        return redirect('list_allocations')

    if location.payment_status == 'paid':
        messages.error(request, "Cannot reject a paid booking.")
        return redirect('list_allocations')

    # Update status to rejected
    location.payment_status = 'rejected'
    location.save()

    messages.success(request, "Booking has been rejected successfully.")
    return redirect('list_allocations')

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