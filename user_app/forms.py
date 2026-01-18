from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book_title', 'author'] # Ini apa yang user perlu isi