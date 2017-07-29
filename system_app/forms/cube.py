from django import forms
from system_app.models import Cube

class CubeForm(forms.ModelForm):

    class Meta:
        model = Cube
        fields = [
                    'unit',
                    'duration',
                    'promo',
                    'start_date',
                    'end_date',
                    'next_due_date'
                ]
        widgets = {
                    'unit': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Unit'}),
                    'duration': forms.NumberInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Lease duration'}),
                    'promo': forms.NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Promo'}),
                    'start_date': forms.DateInput(format='%m/%d/%Y',
                                                  attrs={'class': 'form-control datepicker',
                                                         'placeholder': 'Starting date of lease'}),
                    'end_date': forms.DateInput(format='%m/%d/%Y',
                                                attrs={'class': 'form-control datepicker',
                                                       'placeholder': 'End date of lease'}),
                    'next_due_date': forms.DateInput(format='%m/%d/%Y',
                                                     attrs={'class': 'form-control datepicker',
                                                            'placeholder': 'Next due date'})
                }