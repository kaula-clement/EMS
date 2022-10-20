from django.shortcuts import render,redirect
from .models import Examiner,Invitation,CustomUser,Staff,Bank,BankBranch
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StaffForm


#======================================

def StaffHome(request): 
    examiners=Examiner.objects.all()
    examiners_count=examiners.count()
    #branches=BankBranch.objects.all()
    available_examiners=examiners.filter(availability=True).count()
    context={
            'examiners_count':examiners_count,
            'available_examiners':available_examiners,
          #  'branches':branches
            }
    return render(request, 'Staff/Staff_home.html',context)


class StaffCreate(LoginRequiredMixin,CreateView):
    model=Staff
    form_class=StaffForm
    template_name='Staff/staff_form.html'
    success_url=reverse_lazy('staff-list')
    def form_valid(self, StaffForm):
        #pre save to get id
        super().form_valid(StaffForm) 
        #create user for the staff
        StaffForm.instance.user=CustomUser.objects.create_user(username=self.request.Post.get('name'),
                            password='password3', email='MicroVich.1@abc.com',
                            user_type=2)
            #return a valid form
        print("User Staff created:")
        print("Usename: ",)
        return super(StaffForm,self).form_valid(StaffForm)
 
 
class StaffExaminerList(LoginRequiredMixin,ListView):
    model=Examiner
    queryset= Examiner.objects.filter(approved=True)
    template_name='Staff/Examiner_list.html'
    context_object_name='examiners' 
    
    
    
    
class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'


class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'