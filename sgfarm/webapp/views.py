from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from . models import Category, Subcategory, Transaction
from . forms import AddCategoryForm, AddSubcategoryForm
from django.db.models import Sum
from .models import UserProfile
from django.contrib.auth.decorators import login_required


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
    

# Reset Password Function

def reset_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("home")

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect("home")

        # Set new password
        request.user.set_password(new_password1)
        request.user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, request.user)

        messages.success(request, "Your password has been updated successfully.")
        return redirect("home")

    return render(request, "reset_password.html")

# Update Profile Function

@login_required
def profile_update(request):
    if not request.user.is_authenticated:
        return redirect("home")

    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # update email
        email = request.POST.get("email")
        if email and email != user.email:
            user.email = email
            user.save()

        # update profile picture
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            profile.profile_pic = profile_pic
            profile.save()

        messages.success(request, "Profile updated successfully ")
        return redirect("home")  # redirect to home or profile page

    return render(request, "home.html", {"user": user, "profile": profile})


# logout function
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You are successfully logged out.')
    return redirect('home')


# Category Methods

# def add_category(request):
#     form = AddCategoryForm(request.POST or None) 
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             if form.is_valid():
#                 add_category = form.save()
#                 messages.success(request,'Category added successfully.')
#                 return redirect('view_category')
#         return render(request,'add_category.html', {'form':form})
#     else:
#         messages.success(request, 'You have to login to add categories.')
#         return redirect('home')

def add_category(request):
    form = AddCategoryForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                category_name = form.cleaned_data.get("category_name").strip()

                # Check if category already exists (case-insensitive)
                exists = Category.objects.filter(
                    category_name__iexact=category_name
                ).exists()

                if exists:
                    messages.warning(request, f"Category '{category_name}' already exists.")
                else:
                    form.save()
                    messages.success(request, f"Category '{category_name}' added successfully.")
                
                return redirect('view_category')
        return render(request, 'add_category.html', {'form': form})
    else:
        messages.error(request, 'You have to login to add categories.')
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
                subcategory_name = form.cleaned_data.get("subcategory_name").strip()

                # Check if subcategory already exists (case-insensitive)
                exists = Subcategory.objects.filter(
                    subcategory_name__iexact=subcategory_name
                ).exists()

                if exists:
                    messages.warning(request, f"Subcategory '{subcategory_name}' already exists.")
                else:
                    form.save()
                    messages.success(request, f"Subcategory '{subcategory_name}' added successfully.")
                
                return redirect('view_subcategory')
        return render(request, 'add_subcategory.html', {'form': form})
    else:
        messages.error(request, 'You have to login to add subcategories.')
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

        # Generate year ranges dynamically from 2025-2026 to 2034-2035
        year_ranges = []
        for start in range(2025, 2035):  # 2025 → 2034
            end = start + 1
            year_ranges.append(f"{start}-{end}")
        
        # Track if any duplicates were found
        duplicates = []
        created_count = 0

        for year in year_ranges:
            exists = Transaction.objects.filter(
                category_id=category_id,
                subcategory_id=subcategory_id,
                year=year
            ).exists()

            if exists:
                duplicates.append(year)  # remember which years already exist
            else:
                Transaction.objects.create(
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    year=year
                )
                created_count += 1

        # Messages for user
        if created_count > 0:
            messages.success(request, f"Row for the subcategory created successfully.")

        if duplicates:
            messages.warning(
                request,
                f"Already exists."
            )
            
        return redirect('view_products', year="2025-2026")  
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
        ).order_by('category_id__category_id')
        
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
# --- Net Income Calculation ---
        net_income = {}

        for key in totals.keys():
            income_val = totals.get(key) or 0
            expense_val = totals2.get(key) or 0

# Make sure values are numbers (replace '' with 0)
        try:
            income_val = float(income_val) if income_val != '' else 0
        except:
            income_val = 0

        try:
            expense_val = float(expense_val) if expense_val != '' else 0
        except:
            expense_val = 0

        net_income[key] = income_val - expense_val

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
        fertilizer_exists = any(value not in (None, '', 0) for value in totals_fertilizer.values())

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

        # Replace None with '' for totals_tractor
        for key, value in totals_tractor.items():
            totals_tractor[key] = value or ''
            
        tractor_exists = any(value not in (None, '', 0) for value in totals_tractor.values())

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
        
        wages_exists = any(value not in (None, '', 0) for value in totals_wages.values())
        

# All Tubewel Total

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
            
        electricity_exists = any(value not in (None, '', 0) for value in totals_electricity.values())

# All Tubewel Total

        totals_tubewel = Transaction.objects.filter(
            category__category_name='Tubewel', year=year
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

        # Replace None with '' for totals_tubewel
        for key, value in totals_tubewel.items():
            totals_tubewel[key] = value or ''
        
        tubewel_exists = any(value not in (None, '', 0) for value in totals_tubewel.values())

# All Spray Total

        totals_spray = Transaction.objects.filter(
            category__category_name='Spray', year=year
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

        # Replace None with '' for totals_tubewel
        for key, value in totals_spray.items():
            totals_spray[key] = value or ''
        
        spray_exists = any(value not in (None, '', 0) for value in totals_spray.values())

# All Implements Total

        totals_implements = Transaction.objects.filter(
            category__category_name='Implements', year=year
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

        # Replace None with '' for totals_implements
        for key, value in totals_implements.items():
            totals_implements[key] = value or ''
        
        implements_exists = any(value not in (None, '', 0) for value in totals_implements.values()) 

# All Construction Total

        totals_construction = Transaction.objects.filter(
            category__category_name='Construction', year=year
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

        # Replace None with '' for totals_construction
        for key, value in totals_construction.items():
            totals_construction[key] = value or ''
        
        construction_exists = any(value not in (None, '', 0) for value in totals_construction.values())   

# All Repair Total

        totals_repair = Transaction.objects.filter(
            category__category_name='Repair', year=year
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

        # Replace None with '' for totals_construction
        for key, value in totals_repair.items():
            totals_repair[key] = value or ''
        
        repair_exists = any(value not in (None, '', 0) for value in totals_repair.values())     

# All Developments Total

        totals_developments = Transaction.objects.filter(
            category__category_name='Development', year=year
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

        # Replace None with '' for totals_construction
        for key, value in totals_developments.items():
            totals_developments[key] = value or ''
        
        developments_exists = any(value not in (None, '', 0) for value in totals_developments.values())   

# All Miscellaneous Total

        totals_misc = Transaction.objects.filter(
            category__category_name='Miscellaneous', year=year
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

        # Replace None with '' for totals_construction
        for key, value in totals_misc.items():
            totals_misc[key] = value or ''
        
        misc_exists = any(value not in (None, '', 0) for value in totals_misc.values())          

        return render(request, 'view_products.html', {
            'income_products': income_products,
            'expense_products': expense_products,
            'totals': totals,
            'totals2': totals2,
            'totals_fertilizer':totals_fertilizer,
            'fertilizer_exists':fertilizer_exists,
            'totals_tractor':totals_tractor,
            'tractor_exists':tractor_exists,
            'totals_wages':totals_wages,
            'wages_exists':wages_exists,
            'totals_electricity':totals_electricity,
            'electricity_exists':electricity_exists,
            'totals_tubewel':totals_tubewel,
            'tubewel_exists':tubewel_exists,
            'totals_spray':totals_spray,
            'spray_exists':spray_exists,
            'totals_implements':totals_implements,
            'implements_exists':implements_exists,
            'totals_construction':totals_construction,
            'construction_exists':construction_exists,
            'totals_repair':totals_repair,
            'repair_exists':repair_exists,
            'totals_developments':totals_developments,
            'developments_exists':developments_exists,
            'totals_misc':totals_misc,
            'misc_exists':misc_exists,
            'net_income':net_income,
            'selected_year': year,
            
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