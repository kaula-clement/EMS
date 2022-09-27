from django.shortcuts import render,redirect
from .models import Examiner,Invitation,CustomUser
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#======================================

class CustomLoginView(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('home')
        #return reverse_lazy('examiner-list')

"""
class Home(LoginRequiredMixin,ListView):
    template_name='index.html'
    model=Examiner
    context_object_name='examiner'

    #to view only the examiner whose the user is loged 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['examiner',]= context['examiner'].filter(user=self.request.user)
        return context
 
"""
@login_required()
def Home(request):
    #examiner_obj=Examiner.objects.get(ExaminerCode=request.user.user_id)
    notifications=Invitation.objects.filter(toAddress=request.user.id)
    T_nots=notifications.count()
    context={'notifications':notifications,'T_nots':T_nots}
    return render(request, 'index.html',context)
'''    
def sendInvitation(request,UserID):
    fromUser=request.user
    toUser=User.objects.get(id=UserID)
'''

class ExaminerList(LoginRequiredMixin,ListView):
    model=Examiner
    context_object_name='examiners'


class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'



class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'

class ExaminerCreate(LoginRequiredMixin,CreateView):
    model=Examiner
    #fields='__all__'
    fields=['subject','position','name','Address','District','Province',
                'AccountDetails','NRC','TPIN','cell_Number','email']
    success_url=reverse_lazy('examiner-list')
 

class ExaminerUpdate(LoginRequiredMixin,UpdateView):
    model=Examiner
    fields='__all__'
    success_url=reverse_lazy('examiner-list')

class ExaminerDelete(LoginRequiredMixin,DeleteView):
    model=Examiner
    context_object_name='Examiner'
    success_url=reverse_lazy('examiner-list')

class UserView(LoginRequired,ListView):
    model=CustomUser
    context_object_name="users"
    template_name="users_list.html"