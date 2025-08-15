from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import Category, Subcategory, Transaction
from . forms import AddCategoryForm, AddSubcategoryForm
from django.db.models import F, Value
from django.db.models import FloatField
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db import connection


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


# Category Methods

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
        
        category_record = Category.objects.all()
        return render(request, 'view_category.html',{'category_record':category_record})
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')

def delete_category(request, pk):
    if request.user.is_authenticated:
        
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
    
    # SubCategory Methods

def add_subcategory(request):
    form = AddSubcategoryForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_subcategory = form.save()
                messages.success(request,'Subcategory added successfully.')
                return redirect('view_subcategory')
        return render(request,'add_subcategory.html', {'form':form})
    else:
        messages.success(request, 'You have to login to add subcategories.')
        return redirect('home')

def view_subcategory(request):
    if request.user.is_authenticated:

        subcategory_record = Subcategory.objects.all()
        return render(request, 'view_subcategory.html',{'subcategory_record':subcategory_record})
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')

def delete_subcategory(request, pk):
    if request.user.is_authenticated:
        
        subcategory_delete = get_object_or_404(Subcategory, pk=pk)
        subcategory_delete.delete()
        messages.success(request, "Subcategory deleted successfully.")
        return redirect('view_subcategory')
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')

def update_subcategory(request, pk):
    if request.user.is_authenticated:
        subcategory_instance = get_object_or_404(Subcategory, pk=pk)
        form = AddSubcategoryForm(request.POST or None, instance=subcategory_instance)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Sub-Category updated successfully.")
                return redirect('view_subcategory')

        return render(request, 'update_subcategory.html', {'form': form})
    else:
        messages.warning(request, 'You have to login.')
        return redirect('home')

#  Transaction Methods

def add_products(request):
    
    if request.user.is_authenticated:
        categories = Category.objects.all()
        return render(request, 'add_products.html',{'categories':categories})

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('subcategory_id', 'subcategory_name')
    return JsonResponse(list(subcategories), safe=False)

def add_row(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        subcategory_id = request.POST.get("subcategory")
        year = request.POST.get("year")

        # Save to database
        Transaction.objects.create(
            category_id=category_id,
            subcategory_id=subcategory_id,
            year=year
        )

        messages.success(request, "Data saved successfully!")
        return redirect('view_products', year=year)  # redirect to your desired page
    else:
        messages.warning(request, 'You have to login.')
        return redirect('home')

def view_products(request, year):
    if request.user.is_authenticated:
        income_products = Transaction.objects.filter(
            category__category_type=1, year=year
        ).order_by('category_id')

        expense_products = Transaction.objects.filter(
            category__category_type=2, year=year
        ).order_by('category_id__category_name')
        
# All Income Total

        totals = Transaction.objects.filter(
            category__category_type=1, year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )
        

        # Replace None with '' for totals
        for key, value in totals.items():
            totals[key] = value or ''

# All Expenditures Total
        
        totals2 = Transaction.objects.filter(
            category__category_type=2, year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )

        # Replace None with 0 for totals2
        for key, value in totals2.items():
            totals2[key] = value or ''

# All Fertilizer Total

        totals_fertilizer = Transaction.objects.filter(
            category__category_name='Fertilizer', year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )

        # Replace None with '' for totals_fertilizer
        for key, value in totals_fertilizer.items():
            totals_fertilizer[key] = value or ''

# All Tractor Total

        totals_tractor = Transaction.objects.filter(
            category__category_name='Tractor', year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )

        # Replace None with '' for totals_fertilizer
        for key, value in totals_tractor.items():
            totals_tractor[key] = value or ''

# All Wages Total

        totals_wages = Transaction.objects.filter(
            category__category_name='Wages', year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )

        # Replace None with '' for totals_wages
        for key, value in totals_wages.items():
            totals_wages[key] = value or ''
        
# All Electricity Total

        totals_electricity = Transaction.objects.filter(
            category__category_name='Electricity', year=year
        ).aggregate(
            total_jul_1_a=Sum('jul_1_a'),
            total_jul_2_a=Sum('jul_2_a'),
            total_aug_1_a=Sum('aug_1_a'),
            total_aug_2_a=Sum('aug_2_a'),
            total_sep_1_a=Sum('sep_1_a'),
            total_sep_2_a=Sum('sep_2_a'),
            total_oct_1_a=Sum('oct_1_a'),
            total_oct_2_a=Sum('oct_2_a'),
            total_nov_1_a=Sum('nov_1_a'),
            total_nov_2_a=Sum('nov_2_a'),
            total_dec_1_a=Sum('dec_1_a'),
            total_dec_2_a=Sum('dec_2_a'),
            total_jan_1_a=Sum('jan_1_a'),
            total_jan_2_a=Sum('jan_2_a'),
            total_feb_1_a=Sum('feb_1_a'),
            total_feb_2_a=Sum('feb_2_a'),
            total_mar_1_a=Sum('mar_1_a'),
            total_mar_2_a=Sum('mar_2_a'),
            total_apr_1_a=Sum('apr_1_a'),
            total_apr_2_a=Sum('apr_2_a'),
            total_may_1_a=Sum('may_1_a'),
            total_may_2_a=Sum('may_2_a'),
            total_jun_1_a=Sum('jun_1_a'),
            total_jun_2_a=Sum('jun_2_a'),
            total=Sum('total'),
        )

        # Replace None with '' for totals_wages
        for key, value in totals_electricity.items():
            totals_electricity[key] = value or ''



        return render(request, 'view_products.html', {
            'income_products': income_products,
            'expense_products': expense_products,
            'totals': totals,
            'totals2': totals2,
            'totals_fertilizer':totals_fertilizer,
            'totals_tractor':totals_tractor,
            'totals_wages':totals_wages,
            'totals_electricity':totals_electricity,
            'selected_year': year
        })

    else:
        messages.success(request, 'You have to login.....')
        return redirect('home')



def make_transaction(request, pk):
    transaction = get_object_or_404(Transaction.objects.select_related('subcategory'), pk=pk)

    if not request.user.is_authenticated:
        messages.success(request, 'You have to login.....')
        return redirect('home')

    if request.method == 'POST':
        selected_month = request.POST.get('month')
        qty = request.POST.get('qty')
        rate = request.POST.get('rate')

        if not selected_month or not qty or not rate:
            return render(request, 'make_transaction.html', {
                'transaction': transaction,
                'error': 'Missing month, qty, or rate'
            })

        try:
            qty = float(qty)
            rate = float(rate)
        except (TypeError, ValueError):
            return render(request, 'make_transaction.html', {
                'transaction': transaction,
                'error': 'Invalid quantity or rate'
            })

        amount = qty * rate

        qty_field = f"{selected_month}_q"
        rate_field = f"{selected_month}_r"
        amount_field = f"{selected_month}_a"

        setattr(transaction, qty_field, qty)
        setattr(transaction, rate_field, rate)
        setattr(transaction, amount_field, amount)
  
        transaction.save()

        messages.success(request, 'Transaction updated successfully.')

    return render(request, 'make_transaction.html', {'transaction': transaction})

def delete_transaction(request, pk):
    if request.user.is_authenticated:
        transaction_delete = get_object_or_404(Transaction, pk=pk)
        
        year = transaction_delete.year  
        
        transaction_delete.delete()
        messages.success(request, "Record deleted successfully.")
        
        return redirect('view_products', year=year)  
    else:
        messages.success(request,'You have to login.....')
        return redirect('home')