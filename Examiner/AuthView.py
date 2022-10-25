from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from requests import request
from .models import CustomUser,EAD,Examiner,Province,Staff,Bank
from .forms import EADForm, ExaminerForm, StaffForm, UserForm
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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
    form_class=UserForm
    context_object_name= 'User'
    template_name='EAD/userManager.html' 
    success_url=reverse_lazy('userlist') 
    
class ProfileUpdate(UpdateView):
    model=EAD
    form_class=EADForm
    context_object_name='ead'
    template_name='EAD/update_profile.html'
    success_url= reverse_lazy('login')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['provinces']=Province.objects.all()
        context['banks']=Bank.objects.all()
        return context

    
def updateprofile(request,pk): 
    if request.user.user_type==1:
        User=EAD.objects.get(user=pk)
        form=EADForm(instance=User)
    elif request.user.user_type==2:
        User=Staff.objects.get(user=pk)
        form=StaffForm(instance=User)
    elif request.user.user_type==3:
        User=Examiner.objects.get(user=pk)
        form=ExaminerForm(instance=User)
    #print("============EAD:",User)
    provinces=Province.objects.all()
    
    context={
        'form':form,
        'provinces':provinces,
            }
    
    if request.method=="POST":
        if request.user.user_type==1:
            User=EAD.objects.get(user=pk)
            form=EADForm(request.POST,instance=User)
        elif request.user.user_type==2:
            User=Staff.objects.get(user=pk)
            form=StaffForm(request.POST,instance=User)
        elif request.user.user_type==3:
            User=Examiner.objects.get(user=pk)
            form=ExaminerForm(request.POST,instance=User)
            
        if form.is_valid():
            form.save()
            messages.success(request, "Your password was successfully updated!")
            return redirect('login')
        else:
            return HttpResponse("profile Update failed")
        
    return render(request,'EAD/update_profile.html',context)



def updatepassword(request):
    form=PasswordChangeForm(request.user)
    context={
        'form':form,
    }  
    if request.method=='POST':
        form=PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('updateprofile' ,pk=request.user.id)
        else:
             return HttpResponse("Error changing password")
            
    return render(request,'EAD/password_change.html',context)
        
  