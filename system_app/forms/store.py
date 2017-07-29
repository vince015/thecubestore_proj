from django import forms
from system_app.models import Store

class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = [
                    'name',
                    'product',
                    'facebook',
                    'instagram',
                    'website',
                ]
        widgets = {
                    'name': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Store\'s name'}),
                    'product': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Product'}),
                    'facebook': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Store\'s Facebook page'}),
                    'instagram': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Store\'s Instagram page'}),
                    'website': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder':'Store\'s website'}),
                }