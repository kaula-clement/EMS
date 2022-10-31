import http
from django.shortcuts import render,redirect,HttpResponse
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from requests import put, request
from .models import Bank, Examiner,Invitation, Staff,Subject,Position,EAD,CustomUser,Province
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import is_valid_path, reverse_lazy
from . forms import EADForm,InvitationForm,ExaminerForm, UserForm,ChangePassword
#======================================
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from . decorators import unauthenticated_user,allowed_users
#======================================

#@login_required()
@ unauthenticated_user
def EADHome(request): 
    examiners=Examiner.objects.all()
    examiners_count=examiners.count()
    staffs=Staff.objects.all()
    staffs_count=staffs.count()
    approved_examiners=examiners.filter(approved=True).count()
    available_examiners=examiners.filter(availability=True).count()
    subject_count=Subject.objects.all().count()
    context={
            'examiners_count':examiners_count,
            'subject_count':subject_count,
            'staffs_count':staffs_count,
            'available_examiners':available_examiners,
            'approved_examiners':approved_examiners
            }
    print("Im in the right view +++++++++++++++++++")
    return render(request, 'EAD/EAD_home.html',context)

class EADCreateView(CreateView):
    model=EAD
    form_class=EADForm
    template_name='EAD/EAD_Create.html'
    success_url=reverse_lazy('ead-list')


class EADListView(ListView):
    model=EAD
    context_object_name='EADs'
    template_name='EAD/EAD_List.html'

class EADUpdateView(UpdateView):
    model=EAD
    fields=('firstName','LastName','UserName')
    template_name='EAD/EAD_Create.html'
    success_url = reverse_lazy('subject-list')

class EADDeleteView(DeleteView):
    model=EAD
    context_object_name='obj'
    template_name='Subject/confirm_Delete.html'
    success_url=reverse_lazy('ead-list')

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


class ExaminerCreate(LoginRequiredMixin,CreateView):
    model=Examiner
    form_class=ExaminerForm 
    template_name='EAD/Examiner_form.html'
    success_url=reverse_lazy('examiner-list')
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['subject_list']=Subject.objects.all()
        context['province_list']=Province.objects.all()
        context['position_list']=Position.objects.all()
        context['bank_list']=Bank.objects.all()
        return context
    def form_valid(self, ExaminerForm):
        td=str(date.today().year)
        #pre save to get id
        super().form_valid(ExaminerForm)
        #concatenate year(2digits)+[subject code]+ [id] to make code
        code=td[-2:]+'-'+ExaminerForm.instance.subject.subjectCode+str(self.object.id)
        #Examinercode is = concatenated code 
        ExaminerForm.instance.ExaminerCode=code
        #create user for the examiner
        first_name=ExaminerForm.instance.first_name
        last_name=ExaminerForm.instance.last_name
        ExaminerForm.instance.user=CustomUser.objects.create_user(username=code,
                                                                  first_name=first_name,
                                                                  last_name=last_name,
                            password='password3', email='MicroVich.1@abc.com',
                            user_type=3)
                #return a valid form
        return super(ExaminerCreate,self).form_valid(ExaminerForm)



class ExaminerList(LoginRequiredMixin,ListView):
    model=Examiner
    template_name='EAD/Examiner_list.html'
    context_object_name='examiners'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['available_examiners']=Examiner.objects.filter(availability=True)
        context['approved_examiners']=context['available_examiners'].filter(approved=True)
        return context
        
    
    
    def post(self,request,*args, **kwargs):
        if request.method=="POST":
            Examiner.objects.filter(id__in=request.POST.getlist('id[]')).delete()
        return redirect('examiner-list')
    
def examinerRequests(request):
    examiners=Examiner.objects.filter(approved=False)
    ead=EAD.objects.get(user=request.user)
    context={
        'examiners':examiners
    }
    if request.method=='POST':
        toApprove=request.POST.getlist('id[]')
        for item in toApprove:
            examiner=Examiner.objects.get(pk=item)
            if examiner.availability==True:                
                try:
                    examiner.approved=True
                    examiner.save()
                    letter=Invitation.objects.create(toAddress=examiner,fromAddress=ead,title="Tiltle of the new invitation letter",
                                                    msg="the message is ryt here ..wooo")
                    letter.save()
                except:
                    print("coudn't approve",examiner)
                try:
                    send_mail(
                        'ECZ Examiner application approval',
                        'Hellow Examiner,Your application has been approved.Thank you',
                        'microvich@zohomail.com',
                        [examiner.email],
                        fail_silently=False,
                    )
                except:
                    print("couldn't send email to:",examiner.email)
                    
        return redirect('examiner-requests')
        
    return render(request,'Examiner/examinerRequests.html',context)
        

class ExaminerUpdate(LoginRequiredMixin,UpdateView):
    model=Examiner
    form_class=ExaminerForm
    template_name='EAD/Examiner_form.html'
    success_url=reverse_lazy('examiner-list')

class ExaminerDelete(LoginRequiredMixin,DeleteView):
    print("Deleting view for EAD")
    model=Examiner
    context_object_name='Examiner'
    success_url=reverse_lazy('examiner-list')
    

class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    form_class=ExaminerForm
    context_object_name='Examiner'      
        
class EADUpdate(UpdateView):
    model=CustomUser
    fields="__all__"
    context_object_name='ead'
    template_name='EAD/update_profile.html'
    success_url=reverse_lazy('ead-list')
    

def updateprofilesave(request):
    print("Im in saving method =============")
    if request.method=="POST":
        print("getting post data")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        province=request.POST.get('province')
        district=request.POST.get('district')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            print("Replacing post data")
            customuser = CustomUser.objects.get(id=request.user.id)
            print("Replacing post data for USER: ",customuser)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)    
            form=form(request.Post)
            if form.is_valid():
                form.save()   
            ead = EAD.objects.get(user=customuser.id)
            ead.address = address
            ead.province=province
            ead.district=district
            
            
            customuser.save()
            ead.save()
        
            print("EAD Profile updated: ",ead.address)
            #messages.success(request, "Profile Updated Successfully")
            return redirect('profile')
        except:
            pass
            #messages.error(request, "Failed to Update Profile")
            return redirect('profile')



class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'

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
   