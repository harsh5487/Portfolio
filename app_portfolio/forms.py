from django import forms
from django.forms import widgets,ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Stock

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_name' , 'stock_date', 'stock_quant']
        widgets = {'stock_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder':'Select a date'})}

class SellForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['sell_price', 'sell_date', 'sell_quant']
        widgets = {'sell_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Select a date'})}
