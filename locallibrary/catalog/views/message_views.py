from ..models import Item_request, Request_message, User_alert
from ..forms import CustMesForm, UserAlertForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

def CustMes(request, pk):
    if request.POST:
        form = CustMesForm(request.POST)
        req = get_object_or_404(Item_request, pk=pk)
        if form.is_valid():
            req.is_accepted = False
            req.save()
            mes = Request_message()
            mes.request = Item_request.objects.get(pk=pk)
            mes.message = 'Your request for '+str(req.item)+' has been denied. '
            mes.save()
            addmes = Request_message.objects.get(pk=mes.pk)
            addmes.message += ' ---   Message: ' + form.cleaned_data['message']
            addmes.save()
            return HttpResponseRedirect('/')
    else:
        form = CustMesForm()
    return render(request, 'catalog/cust_mes.html', {'form': form})

def AckMessage(request, pk):
    mes = get_object_or_404(Request_message, pk=pk)
    if request.method == 'POST':
        mes.is_viewed = True
        mes.save()
        return HttpResponseRedirect('/catalog/')
    else:

        return HttpResponseRedirect('/catalog/')

def UserAlertView(request):
    if request.POST:
        form = UserAlertForm(request.POST)
        if form.is_valid():
          obj, created = User_alert.objects.update_or_create(
            user = request.user,
          defaults = {'alert_type' : form.cleaned_data['alert_type']}
          )
          return HttpResponseRedirect('/')
    else:
      form = UserAlertForm()
    return render(request, 'catalog/user_alerts.html', {'form': form})
