from django import forms
from system_app.models import Payout

class PayoutForm(forms.ModelForm):

    class Meta:
        model = Payout
        fields = [
                    'reference_number',
                    'date',
                    'amount',
                    'remarks'
                ]
        widgets = {
                    'reference_number': forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Reference number'}),
                    'date': forms.DateInput(format='%m/%d/%Y',
                                            attrs={'class': 'form-control datepicker',
                                                   'placeholder': 'Date of payout'}),
                    'amount': forms.NumberInput(attrs={'step': 0.01,
                                                       'value': 0.00,
                                                       'class': 'form-control',
                                                       'placeholder': 'Amount deposited'}),
                    'remarks': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Remarks'})
                }