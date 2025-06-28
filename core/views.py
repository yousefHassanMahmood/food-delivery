from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Restaurant
import bcrypt

def signup_view(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('core:signup')

        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(),
            bcrypt.gensalt()
        ).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'].strip(),
            last_name  = request.POST['last_name'].strip(),
            email      = request.POST['email'].strip(),
            password   = pw_hash,
            address    = request.POST.get('address','').strip(),
            phone      = request.POST.get('phone','').strip(),
        )
        request.session['user_id'] = user.id
        messages.success(request, "Account created and logged in!")
        return redirect('core:home')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email','').strip()
        password = request.POST.get('password','')
        user_qs = User.objects.filter(email=email)
        if user_qs:
            user = user_qs.first()
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('core:home')

        messages.error(request, "Invalid email or password.")
        return redirect('core:login')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('core:login')


def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {
        'restaurants': restaurants,
    })


def menu_view(request, id):
    # TODO: fetch the Restaurant & its menu items by `id`
    return render(request, 'menu.html', {'restaurant_id': id})

def cart_view(request):
    # TODO: render the user’s cart contents
    return render(request, 'cart.html')

def tracking_view(request, order_id):
    # TODO: fetch order status by `order_id`
    return render(request, 'tracking.html', {'order_id': order_id})

def about_view(request):
    return render(request, 'about.html')
