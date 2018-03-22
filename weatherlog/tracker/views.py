from django.shortcuts import render
from .forms import SignUpForm, AddLocationForm, CreateJournalForm, DateRecordForm
from django.contrib.auth import login, authenticate
from .models import User, Location, Journal, Date_record
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        journal_list=Journal.objects.filter(user=request.user)
        return render(
            request,
            'index.html',
            context={'journal_list' :journal_list}
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

def AddLocation(request):
    if request.method == 'POST':
      form = AddLocationForm(request.POST)
      if form.is_valid():
          LocMod = Location()
          LocMod.locality_name = form.cleaned_data.get('locality_name')
          LocMod.zip = form.cleaned_data.get('zip')
          LocMod.save()
          return HttpResponseRedirect('/tracker/')
      else:
          return HttpResposnseRedirect('/tracker/')
    else:
        form = AddLocationForm()
    return render(request, 'tracker/add_location.html', {'form' : form})

def CreateJournal(request):
    if request.method == 'POST':
      form = CreateJournalForm(request.POST)
      if form.is_valid():
          JourMod = Journal()
          JourMod.user = request.user
          JourMod.locality = form.cleaned_data.get('locality')
          JourMod.description = form.cleaned_data.get('description')
          JourMod.save()
          return HttpResponseRedirect('/tracker/')
      else:
          return HttpResposnseRedirect('/tracker/')
    else:
        form = CreateJournalForm()
    return render(request, 'tracker/create_journal.html', {'form' : form})

def CreateDateRecord(request):
    if request.method == 'POST':
        form = DateRecordForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/tracker/')
    else:
        form = DateRecordForm()
    return render(request, 'tracker/create_date_record.html', {'form' : form})
