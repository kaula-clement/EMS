from django.shortcuts import render,redirect
from .models import Examiner,Invitation,Subject,Position,EAD
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from . forms import EADForm,InvitationForm,ExaminerForm
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#======================================


@login_required()
def Home(request):
    #examiner_obj=Examiner.objects.get(ExaminerCode=request.user.user_id)
    notifications=Invitation.objects.filter(toAddress=request.user.id)
    T_nots=notifications.count()
    context={'notifications':notifications,'T_nots':T_nots}
    return render(request, 'index.html',context)

class EADCreateView(CreateView):
    model=EAD
    form_class=EADForm
    template_name='EAD/EAD_Create.html'

class EADListView(ListView):
    model=EAD
    context_object_name='EADs'
    template_name='EAD/EAD_List.html'

class EADDeleteView(DeleteView):
    model=EAD
    context_object_name='obj'
    template_name='Subject/confirm_Delete.html'
    success_url=reverse_lazy('ead-list')

class EADUpdateView(UpdateView):
    model=EAD
    fields=('firstName','LastName','UserName')
    template_name='EAD/EAD_Create.html'
    success_url = reverse_lazy('subject-list')



def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')



class SubjectCreateView(CreateView):
    model=Subject
    fields='__all__'
    template_name='Subject/Subject_Create.html'
    success_url=reverse_lazy('subject-list')

class SubjectListView(ListView):
    model=Subject
    context_object_name='subjects'
    template_name='Subject/Subject_List.html'

class SubjectUpdateView(UpdateView):
    model=Subject
    fields='__all__'
    template_name='Subject/Subject_Create.html'
    success_url = reverse_lazy('subject-list')

class SubjectDeleteView(DeleteView):
    model=Subject
    context_object_name='subject'
    template_name='Subject/confirm_Delete.html'
    success_url=reverse_lazy('subject-list')

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
    form_class=ExaminerForm
    context_object_name='Examiner'
"""
class ExaminerCreate(LoginRequiredMixin,CreateView):
    model=Examiner
    #fields='__all__'
    fields=['subject','position','name','Address','District','Province',
                'AccountDetails','NRC','TPIN','cell_Number','email']
    success_url=reverse_lazy('examiner-list')
 """

class ExaminerUpdate(LoginRequiredMixin,UpdateView):
    model=Examiner
    fields='__all__'
    success_url=reverse_lazy('examiner-list')

class ExaminerDelete(LoginRequiredMixin,DeleteView):
    model=Examiner
    context_object_name='Examiner'
    success_url=reverse_lazy('examiner-list')

class InviteView(CreateView):
    model=Invitation
    form_class=InvitationForm
    template_name='Examiner/Invite.html'
    success_url=reverse_lazy('notifications-list')
    

class invitationResponse(LoginRequiredMixin,UpdateView):
    model=Invitation
    template_name='confirm_Invitation.html'
    fields='__all__'
    context_object_name='invitation'
    success_url=reverse_lazy('home')

@login_required()
def invitation_approve(request, inv_id):
    invitation = Invitation.objects.get(id=inv_id)
    invitation.StatusConfirm = 1
    invitation.save()
    return redirect('home')

@login_required()
def invitation_reject(request, inv_id):
    invitation = Invitation.objects.get(id=inv_id)
    invitation.StatusConfirm = 2
    invitation.save()
    return redirect('home')
   