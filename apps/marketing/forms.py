from django import forms
from .models import Product, Inventory, Orders

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'unit', 'unit_price']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['plant', 'image', 'quantity', 'unit', 'unit_price', 'pr_date', 'ex_date', 'inventory_state']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['user', 'type', 'quantity', 'unit', 'total_price', 'status']



