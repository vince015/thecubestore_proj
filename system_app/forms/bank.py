from django import forms
from system_app.models import Bank

class BankForm(forms.ModelForm):

    class Meta:
        model = Bank
        fields = [
                    'owner',
                    'bank',
                    'account',
                ]
        widgets = {
                    'owner': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Bank account owner\'s name'}),
                    'bank': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Bank\'s name'}),
                    'account': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Bank account number'}),
                }
