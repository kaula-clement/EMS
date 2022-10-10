from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from .models import Examiner,Invitation,Subject,Position,EAD,CustomUser,Province
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user.user_type
        if user == 1:
            return reverse_lazy('ead-home')
        elif user == 2:
             return reverse_lazy('staff-home')
        else:
            return reverse_lazy('Examiner-home')

class CustomGroupList(LoginRequiredMixin,ListView):
    model=Group
    context_object_name='groups'
    template_name ='EAD/Groups.html'

class CustomUserList(LoginRequiredMixin,ListView):
    model=CustomUser
    context_object_name='Users'
    template_name='EAD/userList.html'

class CustomUserUpdate(LoginRequiredMixin,UpdateView):
    model=CustomUser
    fields='__all__'
    context_object_name= 'User'
    template_name='EAD/userManager.html' 
    success_url=reverse_lazy('userlist') 
  