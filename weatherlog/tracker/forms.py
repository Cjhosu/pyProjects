from django import forms
from django.forms import ModelForm
from .models import Location, Journal, Date_record
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class AddLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class CreateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('description','locality')

class DateRecordForm(forms.ModelForm):
    class Meta:
        model = Date_record
        fields = ('log_date', 'cloud_cover_type', 'high_temp', 'low_temp')
