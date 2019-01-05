from .loan_views import SetBorrower
from ..forms import InactiveUserForm, SignUpForm, UpdateUserForm
from ..models import Item_status, User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,reverse,get_object_or_404

def CreateInactiveUser(request):
    if request.method == 'POST':
        form = InactiveUserForm(request.POST)
        if form.is_valid():
            newuser = User()
            newuser.username = form.cleaned_data['display_name']
            newuser.first_name = form.cleaned_data['first_name']
            newuser.last_name = form.cleaned_data['last_name']
            newuser.is_active = 'f'
            newuser.save()
            if request.session['pk'] != None:
                pk = request.session['pk']
                SetBorrower(request, pk, newuser)
            return HttpResponseRedirect('/catalog/mybooks')
    else:
        form = InactiveUserForm()
        return render(request, 'catalog/inactive_user.html', {'form': form})

def isInactiveUser(request, fname, lname):
    try:
        checkuser = User.objects.get(first_name = fname , last_name= lname, is_active = 'f')
        return checkuser.id
    except:
        checkuser = None
        return checkuser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email']
            request.session['username'] = form.cleaned_data['username']
            request.session['password'] = form.cleaned_data.get('password1')
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            if isInactiveUser(request, fname, lname) == None:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                adduser = User.objects.get(username=username)
                adduser.email = form.cleaned_data['email']
                adduser.first_name = fname
                adduser.last_name = lname
                adduser.save()
                login(request, user)
                return redirect('index')
            else:
                pk = isInactiveUser(request, fname, lname)
                return redirect('/catalog/convert_user/'+str(pk) )
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def ConvertInactiveUser(request, pk):
    userinst = get_object_or_404(User ,pk=pk)
    email = request.session.get('email')
    username = request.session.get('username')
    password = request.session.get('password')
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            userinst.email = form.cleaned_data['email']
            userinst.is_active = True
            userinst.username = form.cleaned_data['username']
            userinst.set_password(password)
            userinst.save()
            user = authenticate(username=userinst.username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UpdateUserForm(initial={'email':email, 'username':username})
        fname = userinst.first_name
        return render(request,'catalog/convert_user.html',{'form': form ,'fname':fname})
