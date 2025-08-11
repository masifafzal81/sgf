from django.db import models
import datetime

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.category_name}")   
     
class Subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    
    category = models.ForeignKey(
        Category,
        to_field='category_id',
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    subcategory_name = models.CharField(max_length=100)
    subcategory_desc = models.CharField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.subcategory_name}")    
    

def current_year():
    return datetime.datetime.now().year


class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    year = models.CharField(max_length=50,
        choices=[(y, y) for y in range(2025, 2046)],
        default=current_year
    )

    MONTHS = [
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'
    ]

    for month in MONTHS:
        for half in ['1', '2']:
            for suffix in ['q', 'r', 'a']:
                field_name = f"{month.lower()}_{half}_{suffix}"
                locals()[field_name] = models.FloatField(
                    default=0  # default to zero instead of null
                )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        for month in self.MONTHS:
            for half in ['1', '2']:
                qty_field = f"{month.lower()}_{half}_q"
                rate_field = f"{month.lower()}_{half}_r"
                amt_field = f"{month.lower()}_{half}_a"

                qty = getattr(self, qty_field) or 0
                rate = getattr(self, rate_field) or 0
                setattr(self, amt_field, qty * rate)

        super().save(*args, **kwargs)
    
    total = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Calculate total by summing all amount fields, treating None as 0
        self.total = (
            (self.jul_1_a or 0) +
            (self.jul_2_a or 0) +
            (self.aug_1_a or 0) +
            (self.aug_2_a or 0) +
            (self.sep_1_a or 0) +
            (self.sep_2_a or 0) +
            (self.oct_1_a or 0) +
            (self.oct_2_a or 0) +
            (self.nov_1_a or 0) +
            (self.nov_2_a or 0) +
            (self.dec_1_a or 0) +
            (self.dec_2_a or 0) +
            (self.jan_1_a or 0) +
            (self.jan_2_a or 0) +
            (self.feb_1_a or 0) +
            (self.feb_2_a or 0) +
            (self.mar_1_a or 0) +
            (self.mar_2_a or 0) +
            (self.apr_1_a or 0) +
            (self.apr_2_a or 0) +
            (self.may_1_a or 0) +
            (self.may_2_a or 0) +
            (self.jun_1_a or 0) +
            (self.jun_2_a or 0)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} | {self.subcategory} | {self.year}"