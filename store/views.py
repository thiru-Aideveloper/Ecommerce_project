from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
import razorpay
from django.contrib.auth.decorators import login_required

RAZORPAY_KEY_ID = "rzp_test_SxZUjd83SSYqnS"

RAZORPAY_KEY_SECRET = "kyAUrQ7dOrUlI5Vvmf4ROpCN"

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})


def product_detail(request,id):

    product = get_object_or_404(Product,id=id)
    return render(request,'product_detail.html',{'product':product})


from django.contrib import messages

def register(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error( request,"Username already exists")
            return redirect('register')
        
        User.objects.create_user(username=username,email=email,password=password)
        messages.success(request,"Registration Successful")
        return redirect('login')

    return render(request,'register.html')


def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login( request,user)
            return redirect('home')

    return render(request,'login.html')



def user_logout(request):
    logout(request)
    return redirect('home')

def cart(request):
    cart = request.session.get('cart',[])
    products = Product.objects.filter(id__in=cart)
    total = 0
    for product in products:
        total += product.price
    return render(request,'cart.html',{'products':products,'total':total})



@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request,'orders.html',{'orders':user_orders})


def add_to_cart(request,id):

    cart = request.session.get('cart',[])

    if id not in cart:
        cart.append(id)
    request.session['cart'] = cart

    return redirect('cart')


def remove_cart(request,id):

    cart = request.session.get('cart',[])
    if id in cart:
        cart.remove(id)
    request.session['cart'] = cart
    return redirect('cart')

def checkout(request):

    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(product.price for product in products)

    client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": total * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "products": products,
        "total": total,
        "payment": payment,
        "razorpay_key": RAZORPAY_KEY_ID
    }

    return render(request,'checkout.html',context)

def payment_success(request):

    cart = request.session.get('cart',[])

    products = Product.objects.filter(id__in=cart)

    for product in products:
        Order.objects.create(
            user=request.user,
            product=product,
            amount=product.price,
            payment_id="TEST_PAYMENT",
            status="Paid"
        )
    request.session['cart'] = []

    return render(request,'success.html')


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request,'orders.html',{'orders':user_orders})