from django import forms
from .models import Product, Inventory, Order, Sale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'unit', 'unit_price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("الكمية يجب أن تكون أكبر من 0")
        return quantity

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['plant', 'quantity', 'unit', 'unit_price']

