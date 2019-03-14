from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from restaurant import settings
from django.template.loader import render_to_string
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url="/login")
def addrestaurant(request):  
    if request.method == "POST":  
        form = RestaurantForm(request.POST,request.FILES)  
        if form.is_valid():  
            form.save()  
            return redirect('/')            
    else:  
        form = RestaurantForm()  
    return render(request,'restaurant.html',{'form':form})  

def adddish(request):  
    if request.method == "POST":  
        form = DishForm(request.POST,request.FILES)  
        if form.is_valid():  
            form.save()  
            return redirect('/')            
    else:  
        form = DishForm()  
    return render(request,'dish.html',{'form':form})  



def homepage(request):
    if request.user.is_authenticated:
        return restaurantlist(request)
    else:
        return registration(request)    

def registration(request):
    if request.method=="POST":
        form = userform(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username,
			first_name=first_name,last_name=last_name,
			email=email,password=password)
            subject="Confirmation Mail"
            msg="Dear Sir/Ma'am,thank YOU FOR MORE DETAILS CONTACT VISIT:"
            message = render_to_string('mail_template.html')
            send_mail(subject,msg,settings.EMAIL_HOST_USER,[email],
                    html_message=message)
            messages.success(request, 'Data is Entered')
            return redirect('register')
    else:    
        form = userform()                                                     



        
    return render(request, 'registration.html', {'form':form})

def loginuser(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            
            return redirect('restaurant')
        else:
            return render(request, 'login.html',{'name':username})
            #return HttpResponse('<h1>invalid</h1>') 
    return render(request, 'login.html')

def logoutuser(request):
	logout(request)
	return render(request,'login.html')

def restaurantlist(request):
    restaurant_list = Restaurant.objects.get_queryset().order_by('-id')
    paginator = Paginator(restaurant_list, 2)
    page = request.GET.get('page')
    restaurant = paginator.get_page(page)
	#?page = 2
    context={"restaurants":restaurant}
    print(paginator.page_range)
    #data = Restaurant.objects.all()
    return render(request,'restaurantlist.html',context)


def restaurantdetail(request, id):
    data = Dish.objects.filter(restaurant_name=id)
    return render(request, 'restaurantdetail.html',{'Dishlist':data})