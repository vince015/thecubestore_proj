from django import forms
from system_app.models import Item

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
                    'code',
                    'quantity',
                    'price',
                    'vat',
                    'commission',
                    'description',
                ]
        widgets = {
                    'code': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Item Code'}),
                    'quantity': forms.NumberInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Quantity'}),
                    'price': forms.NumberInput(attrs={'step': 0.01,
                                                      'class': 'form-control',
                                                      'placeholder': 'Price'}),
                    'vat': forms.NumberInput(attrs={'step': 0.01,
                                                    'class': 'form-control',
                                                    'placeholder': 'VAT deduction'}),
                    'commission': forms.NumberInput(attrs={'step': 0.01,
                                                    'class': 'form-control',
                                                    'placeholder': 'Sales commission'}),
                    'description': forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Description'}),
                }