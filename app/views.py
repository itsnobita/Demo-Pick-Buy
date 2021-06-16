from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        essentials = Product.objects.filter(category='E')
        beauty = Product.objects.filter(category='B')
        accessories = Product.objects.filter(category='A')
        cameras = Product.objects.filter(category='C')
        headphones = Product.objects.filter(category='H')
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user)) 
        return render(request, 'app/home.html',
        {'essentials':essentials,'beauty':beauty,'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'cameras':cameras,'headphones':headphones,'accessories':accessories,'laptops':laptops, 'totalitem': totalitem})


class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem': totalitem}) 

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount,'totalitem': totalitem })
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)        

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data) 

def buy_now(request):
 return render(request, 'app/buynow.html')

class ProfileView(View):
    
    def get(self,request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))  
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','totalitem': totalitem})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')       
        return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'}) 
@method_decorator(login_required,name='dispatch')

def buy_now(request):
 return render(request, 'app/buynow.html')




@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem': totalitem})

@login_required
def orders(request):
    totalitem = 0
    op = Order_Placed.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
    return render(request, 'app/orders.html', {'order_placed': op,'totalitem': totalitem})


def mobile(request,data = None):
    totalitem = 0
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Xiomi' or data == 'Samsung' or data=='RealMe' :
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/mobile.html', {'mobiles':mobiles,'totalitem': totalitem})

def topwear(request,data = None):
    totalitem = 0
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Roadster' or data == 'Wrogen' or data=='Nike' :
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/topwear.html', {'topwears':topwears,'totalitem': totalitem})

def buttomwear(request,data = None):
    totalitem = 0
    if data == None:
        buttomwears = Product.objects.filter(category='BW')
    elif data == 'Wrangler' or data == 'PeterEngland' or data=='Levis' or data=='Nike':
        buttomwears = Product.objects.filter(category='BW').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/buttomwear.html', {'buttomwears':buttomwears,'totalitem': totalitem})

def laptop(request,data = None):
    totalitem = 0
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Acer' or data == 'Asus' or data=='Lenovo' :
        laptops = Product.objects.filter(category='L').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/laptop.html', {'laptops':laptops,'totalitem': totalitem})

def headphone(request,data = None):
    totalitem = 0
    if data == None:
        headphones = Product.objects.filter(category='H')
    elif data == 'Mivi' or data == 'BoAt' or data=='Apple' :
        headphones = Product.objects.filter(category='H').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/headphone.html', {'headphones':headphones,'totalitem': totalitem})

def camera(request,data = None):
    totalitem = 0
    if data == None:
        cameras = Product.objects.filter(category='C')
    elif data == 'Canon' or data == 'Nikon' or data=='Sony' :
        cameras = Product.objects.filter(category='C').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/camera.html', {'cameras':cameras,'totalitem': totalitem})

def accessorie(request,data = None):
    totalitem = 0
    if data == None:
        accessories = Product.objects.filter(category='A')
    elif data == 'Cables' or data == 'Chargers' or data=='Covers' :
        accessories = Product.objects.filter(category='A').filter(brand=data)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
    return render(request, 'app/accessorie.html', {'accessories':accessories,'totalitem': totalitem})


def essentials(request,data = None):
    totalitem = 0
    if data == None:
        essentials = Product.objects.filter(category='E')
    elif data == 'FoodandNutritions' or data == 'Home_Essentials' or data=='Home_Utility':
        essentials = Product.objects.filter(category='E').filter(brand=data)    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))    
    return render(request, 'app/essentials.html', {'essentials':essentials, 'totalitem': totalitem})

def beauty(request,data = None):
    totalitem = 0
    if data == None:
        beauty = Product.objects.filter(category='B')
    elif data == 'Skin_care' or data == 'Make-up' or data=='Hair_Care':
        beauty = Product.objects.filter(category='B').filter(brand=data)  
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))      
    return render(request, 'app/beauty.html', {'beauty':beauty,'totalitem': totalitem})

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})  

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user) 
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 40.0
    totalamount = 0.0 
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:    
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount     
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order_Placed(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    