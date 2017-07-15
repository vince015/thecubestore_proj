from django import forms

class MerchantForm(forms.Form):

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

    contact_number = forms.CharField(max_length=13,
                                     required=True,
                                     label='Contact Number',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Contact number (mobile)'}))

    primary_address = forms.CharField(max_length=2048,
                                      label='Address',
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Primary address'}))

    alternate_address = forms.CharField(max_length=2048,
                                        label='Alternate Address',
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Alternate address'}))
 
    storename = forms.CharField(max_length=64,
                                required=True,
                                label='Store Name',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s name'}))
    product = forms.CharField(max_length=128,
                              label='Product Description',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Store\'s products'}))

    facebook = forms.CharField(max_length=64,
                               label='Facebook Page',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s Facebook page'}))

    instagram = forms.CharField(max_length=64,
                                label='Instagram Page',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Store\'s Instagram page'}))
    website = forms.CharField(max_length=64,
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
