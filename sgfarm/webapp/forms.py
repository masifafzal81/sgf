from django import forms
from . models import Category, Subcategory, Transaction
import datetime

class AddCategoryForm(forms.ModelForm):
    category_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category Name'
        })
    )
    
    category_type = forms.ChoiceField(
        choices=[
            ('1', 'Income'),
            ('2', 'Expense')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        fields = ['category_name', 'category_type'] 
        

class AddSubcategoryForm(forms.ModelForm):
    subcategory_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sub Category Name'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category"
    )
    
    subcategory_desc = forms.CharField(
        label="",
        required=False,
        max_length=400,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sub-Category Description'
        })
    )

    class Meta:
        model = Subcategory
        fields = ['subcategory_name', 'category', 'subcategory_desc'] 
        
        
