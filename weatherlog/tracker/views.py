from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from .models import User
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


def index(request):
    return render(
        request,
        'index.html',
)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            adduser = User.objects.get(username=username)
            adduser.email = form.cleaned_data['email']
            adduser.first_name = form.cleaned_data['first_name']
            adduser.last_name = form.cleaned_data['last_name']
            adduser.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
