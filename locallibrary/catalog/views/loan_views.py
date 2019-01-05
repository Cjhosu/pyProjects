from .item_views import RequestItem
from ..forms import OtherActiveUsersForm
from ..models import Item_status, Item_request, Request_message, User
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

def MarkReturned(request, pk):
    item = get_object_or_404(Item_status, pk=pk)
    if request.method == 'POST':
        item.borrower = None
        item.save()
        return HttpResponseRedirect('/catalog/mybooks')
    else:
        return HttpResponseRedirect('/catalog/mybooks/')

def AcceptRequest(request, pk):
    req = get_object_or_404(Item_request, pk=pk)
    if request.method == 'POST':
        req.is_accepted = True
        req.save()
        mes = Request_message()
        mes.request = Item_request.objects.get(pk=pk)
        mes.message = 'Your request for '+str(req.item)+' has been accepted'
        mes.save()
        return HttpResponseRedirect('/catalog/')
    else:
        return HttpResponseRedirect('/catalog/')

def PassBorrower(request, pk):
    item = get_object_or_404(Item_status, pk=pk)
    if request.method == 'POST':
        request.session['pk']=pk
        return HttpResponseRedirect('/catalog/loan_item')
    else:
        return HttpResponseRedirect('/catalog/mybooks/')

def SetBorrower(request, pk, user):
    itemstatus = Item_status.objects.get(pk=pk)
    itemstatus.borrower = user
    itemstatus.save()

def LoanItem(request):
    if request.method == 'POST':
        form = OtherActiveUsersForm(request.user.id, request.POST)
        if form.is_valid():
            pk= request.session['pk']
            userid = form.cleaned_data['user']
            try:
                user = User.objects.get(pk=userid)
            except:
                return HttpResponseRedirect('/catalog/inactive_user/')
            SetBorrower(request, pk, user)
            itemstatus = Item_status.objects.get(pk=pk)
            RequestItem(request,itemstatus.item_id, user)
            FillRequest(request, itemstatus.item_id, user)
            return HttpResponseRedirect('/catalog/mybooks/')
    elif request.method == 'GET':
        pk = request.session['pk']
        form = OtherActiveUsersForm(request.user.id)
        return render(request,'catalog/other_active_users.html', {'form':form})

def FillRequest(request, itemid, borrower):
    itemrequest = Item_request.objects.get(item_id = itemid, requester = borrower, filled_at = None)
    itemrequest.filled_at = datetime.now()
    itemrequest.save()

