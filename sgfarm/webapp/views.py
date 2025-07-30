from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import Category
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
                return redirect('view_category')
        return render(request,'add_category.html', {'form':form})
    else:
        messages.success(request, 'You have to login to add categories.')
        return redirect('home')

def view_category(request):
    if request.user.is_authenticated:
        # Look up the specific client data
        category_record = Category.objects.all()
        return render(request, 'view_category.html',{'category_record':category_record})
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')

def delete_category(request, pk):
    if request.user.is_authenticated:
        # Look up the specific client data
        category_delete = get_object_or_404(Category, pk=pk)
        category_delete.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('view_category')
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')
    
def update_category(request, pk):
    if request.user.is_authenticated:
        category_instance = get_object_or_404(Category, pk=pk)
        form = AddCategoryForm(request.POST or None, instance=category_instance)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully.")
                return redirect('view_category')

        return render(request, 'update_category.html', {'form': form})
    else:
        messages.warning(request, 'You have to login.')
        return redirect('home')

