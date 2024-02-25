from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Flight, Booking
from .forms import BookingForm

def home(request):
    return render(request, 'home.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'user_signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def view_flights(request):
    flights = Flight.objects.all()
    return render(request, 'view_flights.html', {'flights': flights})

@login_required
def book_ticket(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    available_seats = 60 - Booking.objects.filter(flight=flight).count()
    
    if request.method == 'POST':
        if available_seats > 0:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.flight = flight
                booking.save()
                return redirect('my_bookings')
        else:
            return HttpResponse("Sorry, all seats on this flight are booked.")
    else:
        form = BookingForm()
    
    return render(request, 'book_ticket.html', {'form': form, 'flight': flight, 'available_seats': available_seats})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

def admin_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'admin_signup.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        # Fetch all bookings
        bookings = Booking.objects.all()
        # Fetch all flights
        flights = Flight.objects.all()
        # Fetch all users (if needed)
        users = User.objects.all()
        return render(request, 'admin_dashboard.html', {'bookings': bookings, 'flights': flights, 'users': users})
    else:
        # Handling the case where the user is not authorized to view the admin dashboard
        return render(request, 'admin_dashboard.html', {'error_message': 'You are not authorized to view this page'})


@login_required
def add_flight(request):
    if request.method == 'POST':
        flight_number = request.POST['flight_number']
        departure_date = request.POST['departure_date']
        departure_time = request.POST['departure_time']
        Flight.objects.create(flight_number=flight_number, departure_date=departure_date, departure_time=departure_time)
        return redirect('admin_dashboard')
    else:
        return render(request, 'add_flight.html')

@login_required
def remove_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    flight.delete()
    return redirect('admin_dashboard')

@login_required
def user_details(request):
    users = User.objects.all()
    return render(request, 'user_details.html', {'users': users})
