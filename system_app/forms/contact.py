from django import forms
from system_app.models import Contact

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
                    'contact_number',
                    'primary_address',
                    'alternate_address',
                ]
        widgets = {
                    'contact_number': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Contact Number',
                                                             'data-inputmask':"'mask': ['(+63) 999 999 9999 ']",
                                                             'data-mask': True}),
                    'primary_address': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Primary address'}),
                    'alternate_address': forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Alternate address'}),
                }
