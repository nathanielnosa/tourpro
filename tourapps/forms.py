from django import forms

from . models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ['order_by','shipping_address']
        exclude = ['cart','amount','order_status','discount','subtotal','payment_completed','ref']
        Widgets = {
            'ordered_by':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'payment_method':forms.TextInput(attrs={'class':'form-control'}),
        }