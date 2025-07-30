from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import AddCategoryForm

def home(request):
    
   
    # check the logged in user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate the user
    
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('home')        
    
    else:
        return render(request, 'home.html', {})

    
def logout_view(request):
    logout(request)
    messages.success(request, 'You are successfully logged out.')
    return redirect('home')

def add_category(request):
    form = AddCategoryForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_category = form.save()
                messages.success(request,'Category added successfully.')
                return redirect('home')
        return render(request,'add_category.html', {'form':form})
    else:
        messages.success(request, 'You have to login to add categories.')
        return redirect('home')
