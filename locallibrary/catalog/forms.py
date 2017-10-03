from django import forms
from django.forms import ModelForm
from .models import Item_type , Item_status, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddBookForm(forms.Form):
    item_id = forms.IntegerField
    item_name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=255)
    author_first = forms.CharField(max_length=100)
    author_last = forms.CharField(max_length=100)
    isbn = forms.CharField(max_length=15)
    publisher = forms.CharField(max_length=30)
    year = forms.CharField(max_length=4)
    description = forms.CharField(widget=forms.Textarea)

class AddItemForm(forms.Form):
    item_type = forms.ModelChoiceField(queryset=Item_type.objects.all())

class UpdateBorrowerForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
  #  def __str__(self):
   #  return User.name

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
