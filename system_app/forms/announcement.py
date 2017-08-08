from django import forms
from system_app.models import Announcement

class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = [
                    'issue_date',
                    'subject',
                    'detail'
                ]
        widgets = {
                    'issue_date': forms.DateInput(format='%m/%d/%Y',
                                                  attrs={'class': 'form-control datepicker',
                                                         'placeholder': 'Date Issued'}),
                    'subject': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Subject'}),
                    'detail': forms.Textarea(attrs={'class': 'form-control',
                                                    'placeholder': 'Detail'})
                }