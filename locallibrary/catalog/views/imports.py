from ..forms import AddBookForm, UpdateBookForm, AddComicForm, UpdateComicForm, OtherActiveUsersForm, AddItemForm, SignUpForm, IssueBookRequestForm, CustMesForm, InactiveUserForm
from ..models import Item, User, Item_type, Book, Comic, Item_status, Item_request, Request_message
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import UpdateView, FormView
