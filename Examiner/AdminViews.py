import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import update_session_auth_hash
from auditlog.models import LogEntry
from requests import request
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q


@login_required()
def logEntries(request):
    logs = LogEntry.objects.all().order_by('timestamp')
    context={
        'logs':logs,
    }
    
    return render(request,'Admin/logEntries.html',context)