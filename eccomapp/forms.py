from email.mime import image
from django import forms
from .models import Order, Customer
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('ordered_by', 'shipping_address', 'mobile', 'email')


class CustomerRegisterationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ['username', 'email', 'full_name', 'address']

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "username already exists.")
        return uname


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField(widget=forms.FileInput())
