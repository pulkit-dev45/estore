from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem


# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category, Order, OrderItem

def home(request):
    books = Book.objects.all()[:8]
    return render(request, 'home.html', {'books': books})


def shop(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    return render(request, 'shop.html', {'categories': categories, 'books': books})


def category_filter(request, id):
    categories = Category.objects.all()
    books = Book.objects.filter(category=id)
    return render(request, 'shop.html', {'categories': categories, 'books': books})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_detail.html', {'book': book})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    cart[id] = cart.get(id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    books = []
    total = 0

    for id, qty in cart.items():
        book = Book.objects.get(id=id)
        book.qty = qty
        book.subtotal = book.price * qty
        total += book.subtotal
        books.append(book)

    return render(request, 'cart.html', {'books': books, 'total': total})


def remove_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


def increase_qty(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 1) + 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop')

    books = []
    total = 0

    for id, qty in cart.items():
        book = Book.objects.get(id=id)
        book.qty = qty
        book.subtotal = book.price * qty
        total += book.subtotal
        books.append(book)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['name'],
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
            phone=request.POST['phone'],
            total_amount=total
        )

        for book in books:
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=book.qty,
                price=book.price
            )

        request.session['cart'] = {}   # cart clear
        return redirect('shop')

    return render(request, 'checkout.html', {
        'books': books,
        'total': total
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('shop')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop')

    books = []
    total = 0

    for id, qty in cart.items():
        book = Book.objects.get(id=id)
        book.qty = qty
        book.subtotal = book.price * qty
        total += book.subtotal
        books.append(book)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['name'],
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
            phone=request.POST['phone'],
            total_amount=total
        )

        for book in books:
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=book.qty,
                price=book.price
            )

        request.session['cart'] = {}

        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'books': books,
        'total': total
    })


@login_required(login_url='login')
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    # 🔥 subtotal calculate here
    for item in items:
        item.subtotal = item.price * item.quantity

    return render(request, 'order_success.html', {
        'order': order,
        'items': items
    })


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def contact_view(request):
    return render(request,"contactus.html")
def term_view(request):
    return render(request,"term_and_condition.html")
def privacy_view(request):
    return render(request,"policy.html")
