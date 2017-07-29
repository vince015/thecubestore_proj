from django import forms
from system_app.models import Payout

class PayoutForm(forms.ModelForm):

    class Meta:
        model = Payout
        fields = [
                    'date',
                    'amount',
                ]
        widgets = {
                    'date': forms.DateInput(format='%m/%d/%Y',
                                            attrs={'class': 'form-control datepicker',
                                                   'placeholder': 'Date of payout'}),
                    'amount': forms.NumberInput(attrs={'step': 0.25,
                                                       'class': 'form-control',
                                                       'placeholder': 'Amount deposited'}),
                }