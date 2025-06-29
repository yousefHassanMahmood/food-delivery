from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import User, Restaurant,MenuItem,Order,OrderItem,Review
import bcrypt
from django.http import JsonResponse

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

        user_type = int(request.POST.get('user_type', User.CUSTOMER))

        user = User.objects.create(
            first_name = request.POST['first_name'].strip(),
            last_name  = request.POST['last_name'].strip(),
            email      = request.POST['email'].strip(),
            password   = pw_hash,
            address    = request.POST.get('address','').strip(),
            phone      = request.POST.get('phone','').strip(),
            user_type  = user_type,
        )
        if user_type == User.RESTAURANT:
            rest_name = request.POST.get('restaurant_name','').strip()
            rest_desc = request.POST.get('restaurant_description','').strip()
            Restaurant.objects.create(
                owner       = user,
                name        = rest_name or f"{user.first_name}'s Restaurant",
                description = rest_desc,
                address     = user.address,
                phone       = user.phone,
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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('core:login')

    if current_user.user_type == User.RESTAURANT:
        restaurant = Restaurant.objects.filter(owner=current_user).first()
        items = restaurant.menu_items.all() if restaurant else []
        return render(request, 'home.html', {
            'current_user': current_user,
            'restaurant': restaurant,
            'items': items,
        })
    else:
        restaurants = Restaurant.objects.all()
        return render(request, 'home.html', {
            'current_user': current_user,
            'restaurants': restaurants,
        })

def add_or_edit_menu_item(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('core:login')
        user = User.objects.get(id=user_id)

        restaurant = Restaurant.objects.filter(owner=user).first()
        if not restaurant:
            messages.error(request, "No restaurant found for your account.")
            return redirect('core:home')

        item_id = request.POST.get('item_id')
        if item_id:
            item = MenuItem.objects.get(id=item_id, restaurant=restaurant)
        else:
            item = MenuItem(restaurant=restaurant)

        item.name        = request.POST['name']
        item.description = request.POST.get('description', '')
        item.price       = request.POST['price']
        item.image_url   = request.POST.get('image_url', '')
        item.save()

        messages.success(
            request,
            f"Menu item {'updated' if item_id else 'created'} successfully!"
        )
    return redirect('core:home')

def delete_menu_item(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('core:login')

        user = User.objects.get(id=user_id)
        restaurant = Restaurant.objects.filter(owner=user).first()
        if not restaurant:
            messages.error(request, "No restaurant found for your account.")
            return redirect('core:home')

        item_id = request.POST.get('item_id')
        item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
        item.delete()
        messages.success(request, "Menu item deleted successfully!")
    return redirect('core:home')

def menu_view(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')

    restaurant = get_object_or_404(Restaurant, id=id)
    menu_items = restaurant.menu_items.all()

    return render(request, 'menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })
    
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    # (Optional) ensure logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)

    # Grab item and quantity
    item_id  = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))

    item = get_object_or_404(MenuItem, id=item_id)

    # Update session cart: { item_id: qty, ... }
    cart = request.session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + quantity
    request.session['cart'] = cart

    total_qty = sum(cart.values())
    return JsonResponse({'success': True, 'cartCount': total_qty})

def cart_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')

    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for item_id_str, qty in cart.items():
        try:
            item_id = int(item_id_str)
            item = MenuItem.objects.get(id=item_id)
        except (ValueError, MenuItem.DoesNotExist):
            continue  # skip invalid IDs

        subtotal = item.price * qty
        total_price += subtotal

        cart_items.append({
            'item': item,
            'quantity': qty,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def cart_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')

    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for item_id_str, qty in cart.items():
        item = get_object_or_404(MenuItem, id=int(item_id_str))
        subtotal = item.price * qty
        total_price += subtotal
        cart_items.append({
            'item': item,
            'quantity': qty,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            qty = max(1, int(request.POST.get('quantity', 1)))
        except ValueError:
            qty = 1

        cart = request.session.get('cart', {})
        cart[item_id] = qty
        request.session['cart'] = cart

    return redirect('core:cart')


def delete_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart = request.session.get('cart', {})
        cart.pop(item_id, None)
        request.session['cart'] = cart

    return redirect('core:cart')


def checkout(request):
    if request.method != 'POST':
        return redirect('core:cart')

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')
    user = get_object_or_404(User, id=user_id)

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('core:cart')

    first_item = get_object_or_404(MenuItem, id=int(next(iter(cart.keys()))))
    restaurant = first_item.restaurant

    total_price = 0
    for id_str, qty in cart.items():
        mi = get_object_or_404(MenuItem, id=int(id_str))
        total_price += mi.price * qty

    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        delivery_address=user.address,
        total_price=total_price,
        status='Pending'
    )

    # Create OrderItems
    for id_str, qty in cart.items():
        mi = get_object_or_404(MenuItem, id=int(id_str))
        OrderItem.objects.create(
            order=order,
            menu_item=mi,
            quantity=qty,
            unit_price=mi.price
        )

    # Clear the cart
    request.session['cart'] = {}

    messages.success(request, f"Order #{order.id} placed! Status: Pending.")
    return redirect('core:tracking')

def tracking_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('core:login')
    current_user = get_object_or_404(User, id=user_id)

    if current_user.user_type == User.RESTAURANT:
        orders = Order.objects.filter(restaurant__owner=current_user).order_by('-created_at')
    else:
        orders = Order.objects.filter(user=current_user).order_by('-created_at')

    return render(request, 'order_list.html', {
        'orders': orders,
        'current_user': current_user,
    })


def update_order_status(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('core:login')
        current_user = get_object_or_404(User, id=user_id)

        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(
            Order,
            id=order_id,
            restaurant__owner=current_user
        )
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}.")
    return redirect('core:tracking')
def about_view(request):
    return render(request, 'about.html')
def menu_view(request, id):
    # require login
    if not request.session.get('user_id'):
        return redirect('core:login')

    restaurant = get_object_or_404(Restaurant, id=id)
    menu_items = restaurant.menu_items.all()
    reviews    = restaurant.reviews.select_related('user').order_by('-created_at')

    return render(request, 'menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews':    reviews,
    })


def submit_review(request, id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.session.get('user_id'))
        restaurant = get_object_or_404(Restaurant, id=id)

        # Validate rating
        try:
            rating = int(request.POST.get('rating', 0))
            if rating < 1 or rating > 5:
                raise ValueError()
        except ValueError:
            messages.error(request, "Please select a rating between 1 and 5.")
            return redirect('core:menu', id=id)

        comment = request.POST.get('comment','').strip()

        Review.objects.create(
            user= user,
            restaurant= restaurant,
            rating= rating,
            comment= comment
        )
        messages.success(request, "Thanks for your review!")
    return redirect('core:menu', id=id)