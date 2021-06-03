
from django.shortcuts import render,redirect
from django.views import View
from .models import Cart,Customer,OrderPlaced,Product
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category='L')

        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,
        'mobiles':mobiles,'laptops':laptops})
    
    
class Product_details(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

@login_required
def payementdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()

        c.delete()
    return redirect('orders')

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
        else:
            return redirect('orders')

@login_required
def checkout(request):
    if request.user.is_authenticated:
        user=request.user
        address=Customer.objects.filter(user=user)
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                dd=p.product.discounted_price
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
        

    return render(request, 'app/checkout.html',{'amt':dd,'address':address,'cart':cart,'total':total_amount})

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):

 obj=Customer.objects.filter(user=request.user)
 
 return render(request, 'app/address.html',{'data':obj,'active':'btn-primary'})

@login_required
def orders(request):
    obj=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':obj})


def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='samsung' or data=='OnePlus':
        mobiles=Product.objects.filter(category='M').filter(brand=data)


    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data=None):
    if data==None:
        laptops=Product.objects.filter(category='L')
    elif data=='HP' or data=='Apple' or data=='Lenovo':
        laptops=Product.objects.filter(category='L').filter(brand=data)

    return render(request, 'app/laptop.html',{'laptops':laptops})


def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationview(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registrations Successfully!!')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            obj=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            obj.save()
            messages.success(request,'Address is Added Successfully!!.')
            
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
        

    