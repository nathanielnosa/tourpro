from django.conf import settings
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from . models import *

from django.contrib import messages
from . forms import CheckoutForm
from django.db.models import Q
# Create your views here.
def index(request):
    # banner
    banner = Banner.objects.all()
    # main content
    main = Place.objects.all().order_by('-created')
    # paginator
    paginator = Paginator(main,3)
    page_number = request.GET.get('page')
    place_list = paginator.get_page(page_number)

    # numbers of items
    try:
        items = Cart.objects.filter(user = request.user.customer)
        item_count = items.count()
    except:
        items = Cart.objects.all()
        item_count = items.count()

    
    context = {
        'banner':banner,
        'shows':main,
        'paginator':place_list,
        'count':item_count
    }

    return render(request, 'tourapp/index.html',context)

def overview(request,id):
    mains = Place.objects.get(id=id)
    day = mains.get_day
    context = {
        'main':mains,
        'day':day
    }
    return render(request, 'tourapp/overview.html',context)


# search engine
def search(request):
    if request.method == 'GET':
        kword = request.GET.get('futtour')
        main = Place.objects.filter(Q(name__icontains = kword) | Q(destination__icontains = kword))
        context = { 
            'result':main
        }
    return render(request, 'tourapp/search.html',context)


# add product to cart
def addtocart(request,id):
    # get the place
    cart_product = Place.objects.get(id=id)
    # check if cart exists
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)
        this_product_in_cart = cart_item.cartproduct_set.filter(place=cart_product)
        # assign cart to user
        if request.user.is_authenticated and request.user.customer:
                cart_item.customer = request.user.customer
                cart_item.save()
        # end
        # checking if item exist in cart
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.per_person += 1
            cartproduct.subtotal += cart_product.price
            cartproduct.save()
            cart_item.total += cart_product.price
            cart_item.save()
            messages.success(request, 'Item increase in cart')
        # new item in cart
        else:
            cartproduct = CartProduct.objects.create(
                cart=cart_item, place=cart_product, rate=cart_product.price, per_person=1, subtotal=cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()
            messages.success(request, 'New item added to cart')

    else:
        cart_item = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(cart=cart_item, place=cart_product, rate=cart_product.price, per_person=1, subtotal=cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()
        messages.success(request, 'New Item to cart')
    return redirect('index')

# users cart
def myCart(request):
    # session
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)
        # user
        if request.user.is_authenticated and request.user.customer:
                cart_item.customer = request.user.customer
                cart_item.save()
    else:
        cart_item = None

    context ={
        'cart':cart_item
    }

    return render(request, 'tourapp/mycart.html',context)

# manage cart
def manageCart(request,id):
    action = request.GET.get('action')
    
    cart_obj = CartProduct.objects.get(id=id)
    cart= cart_obj.cart

    if action == 'inc':
        cart_obj.per_person +=1
        cart_obj.subtotal += cart_obj.rate
        cart_obj.save()
        cart.total +=cart_obj.rate
        cart.save()
        messages.success(request, 'Item Increased')

    elif action == 'dcr':
        cart_obj.per_person -=1
        cart_obj.subtotal -= cart_obj.rate
        cart_obj.save()
        cart.total -=cart_obj.rate
        cart.save()
        messages.success(request, 'Item Decreased')

        if cart_obj.per_person == 0:
            cart_obj.delete()

    elif action == 'rmv':
        cart.total -=cart_obj.subtotal
        cart.save()
        cart_obj.delete()

    else:
        pass
    return redirect('myCart')

def clearCart(request):
    # session
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        # user
        if request.user.is_authenticated and request.user.customer:
                cart.customer = request.user.customer
                cart.save()

        cart.cartproduct_set.all().delete()
        cart.total = 0
        cart.save()
        messages.success(request, 'Cart is now empty')
    return redirect('myCart')

def checkout(request):
    cart_id = request.session.get('cart_id', None)
    cart_obj = Cart.objects.get(id = cart_id)
    form = CheckoutForm()

    # checking authentication
    if request.user.is_authenticated and request.user.customer:
        pass
    else:
        return redirect('/customer/loginuser/?next=/checkout/')

    if request.method == "POST":
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit = False)
            form.cart = cart_obj
            form.amount = cart_obj.total
            form.subtotal = cart_obj.total
            form.discount = 0
            form.order_status = 'Payment Received'
            paymethod = form.payment_method
            del request.session['cart_id']
            paymethod = form.payment_method
            form.save()

            order = form.id
            if paymethod == 'PayStack':
                return redirect('payment', id =order)
    context = {
        'cart':cart_obj,
        'form':form
    }
    return render(request, 'tourapp/checkout.html',context)


def paymentPage(request,id):
    orders = Order.objects.get(id=id)
    context = {
        'order':orders,
        'paystack_public_key' : settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'tourapp/payment.html',context)


def verify_payment(request:HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Order, ref =ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('dashboard')
