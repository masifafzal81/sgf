from django import forms
from . models import Category

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