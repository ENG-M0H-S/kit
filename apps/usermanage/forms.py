from django import forms
from apps.usermanage.models import Account,Transactions


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = '__all__'
      