from django.shortcuts import render, redirect
from .models import Product,Category
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




# Create your views here.

def category(request,foo):
    # replace hyphens with spaces
    foo = foo.replace('-',' ')
    # grab the category from the url
    try:
        # lookup the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That Category Doesn't Exist"))
        return redirect('home')
    

def product(request,pk):
    product = Product.objects.get(id = pk)
    return render(request, 'product.html',{'product':product})
    


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})


def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome back! You have successfully logged in."))
            return redirect('home')
        else:
            messages.success(request, ("Invalid credentials! Please try again."))
            return redirect('login')
        
        
    else:    
        return render(request, 'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been successfully logged out.."))
    return redirect('login')


def register_user(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save user to the database
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
 
    