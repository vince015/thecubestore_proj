from django import forms
from django.contrib.auth.models import User
from system_app.models import Contact, Store, Bank, Profile

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)

        widgets = {
                    'email': forms.EmailInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Valid e-mail address'}),
                  }

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

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
                    'merchant_id',
                    'remarks'
                ]
        widgets = {
                    'merchant_id': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Merchant ID'}),
                    'remarks': forms.Textarea(attrs={'class': 'form-control',
                                                   'placeholder': 'Remarks'}),
                }

class MerchantForm(forms.Form):

    merchant_id = forms.CharField(max_length=64,
                                  required=True,
                                  label='Merchant ID',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Merchant ID'}))
    username = forms.CharField(max_length=150,
                               min_length=3,
                               required=True,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))

    password = forms.CharField(max_length=150,
                               min_length=8,
                               required=True,
                               label='Password',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Generated password'}))

    email = forms.EmailField(label='E-mail address',
                             required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Valid e-mail address'}))

    firstname = forms.CharField(max_length=30,
                                required=True,
                                label='First name',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'First Name'}))

    lastname = forms.CharField(max_length=30,
                               required=True,
                               label='Last name',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Last Name'}))

    remarks = forms.CharField(max_length=2048,
                              required=False,
                              label='Remarks',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Remarks'}))

    contact_number = forms.CharField(max_length=18,
                                     required=True,
                                     label='Contact Number',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Contact number (mobile)',
                                                                   'data-inputmask':"'mask': ['(+63) 999 999 9999 ']",
                                                                   'data-mask': True}))

    primary_address = forms.CharField(max_length=2048,
                                      required=False,
                                      label='Address',
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Primary address'}))

    alternate_address = forms.CharField(max_length=2048,
                                        required=False,
                                        label='Alternate Address',
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Alternate address'}))

    storename = forms.CharField(max_length=64,
                                required=True,
                                label='Store Name',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s name'}))
    product = forms.CharField(max_length=128,
                              required=False,
                              label='Product Description',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Store\'s products'}))

    facebook = forms.CharField(max_length=64,
                               required=False,
                               label='Facebook Page',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s Facebook page'}))

    instagram = forms.CharField(max_length=64,
                                required=False,
                                label='Instagram Page',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s Instagram page'}))
    website = forms.CharField(max_length=64,
                              required=False,
                              label='Website',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Store\'s website'}))

    bank_name = forms.CharField(max_length=128,
                                required=True,
                                label='Bank Name',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Bank\'s name'}))

    bank_account = forms.CharField(max_length=128,
                                   required=True,
                                   label='Bank Account',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Bank account number'}))

    bank_owner = forms.CharField(max_length=256,
                                 required=True,
                                 label='Bank Account Owner',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Bank account owner\'s name'}))

