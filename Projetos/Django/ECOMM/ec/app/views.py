from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Product, Customer, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Count
from django.contrib import messages
from time import sleep
from django.utils.formats import localize
from django.db.models import Q
from .utils import Moeda

# Create your views here.

def prodincar(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        numprod = 0
        for p in cart:
            numprod +=1
        totalprod = numprod
        return totalprod




def home(request):
    totalprod = prodincar(request)

    return render(request, 'app/home.html', locals())

def about(request):
    totalprod = prodincar(request)
    return render(request, "app/about.html", locals())

def contact(request):
    totalprod = prodincar(request)
    return render(request, "app/contact.html", locals())




class CategoryView(View):
    def get(self, request, val):
        totalprod = prodincar(request)
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values("title")
        return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self, request, val):
        totalprod = prodincar(request)
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values("title")
        return render(request, "app/category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        totalprod = prodincar(request)
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/customerregistration.html", locals()) 


class ProfileView(View):
    def get(self, request):
        totalprod = prodincar(request)
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

def Address(request):
    totalprod = prodincar(request)
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        totalprod = prodincar(request)
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
        
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Updated Address Save Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    c = Cart.objects.filter(user=user)
    products = []
    for p in c:
        products.append(p.product)

    if product in products:
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
    else:
        Cart(user=user, product=product).save()
        return redirect('/cart')

    return redirect('/cart')
    
def show_cart(request):
    totalprod = prodincar(request)
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount=0

    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value


    totalamount = Moeda(amount + 40)
    amount = Moeda(amount)


    return render(request, 'app/addtocar.html', locals())


class checkout(View):
    def get(self, request):
        totalprod = prodincar(request)
        user=request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = Moeda(famount + 40)
        famount = Moeda(famount)
        return render(request, 'app/checkout.html', locals())

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = Moeda(amount + 40)
        amount = Moeda(amount)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))


        if c.quantity > 1:
            c.quantity-=1
            c.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = Moeda(amount + 40)
            amount = Moeda(amount)
            
            
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount,
            }
            return JsonResponse(data)
        else:
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = Moeda(amount + 40)
            amount = Moeda(amount)
            
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount,
            }
            return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = Moeda(amount + 40)
        amount = Moeda(amount)
        data = {
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)