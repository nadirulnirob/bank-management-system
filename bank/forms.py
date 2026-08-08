from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BankAccount


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder_name', 'account_number']

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )