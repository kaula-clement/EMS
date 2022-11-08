from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from datetime import date,datetime
import logging
from django.contrib import messages
#===============local imports
from .models import Bank, Examiner,Invitation, Staff,Subject,Position,EAD,CustomUser,Province,Session
from . forms import EADForm,InvitationForm,ExaminerForm,ExaminerUploadForm
from .filters import ExaminerFilter
#==============Views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView


#======================================
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from . decorators import unauthenticated_user
#======================================

#@login_required()
@ unauthenticated_user
def EADHome(request): 
    examiners=Examiner.objects.all()
    examiner_list=[]
    approved_examiners_list=[]
    examiner_list.append(examiners)
    examiners_count=examiners.count()
    staffs=Staff.objects.all()
    staffs_count=staffs.count()
    approved_examiners=examiners.filter(approved=True).count()
    approved_examiners_list.append(approved_examiners)
    available_examiners=examiners.filter(availability=True).count()
    subject_count=Subject.objects.all().count()
    context={
        'examiner_list':examiner_list,
            'examiners_count':examiners_count,
            'subject_count':subject_count,
            'staffs_count':staffs_count,
            'available_examiners':available_examiners,
            'approved_examiners':approved_examiners
            }
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
        try:
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
            email=ExaminerForm.instance.email
            ExaminerForm.instance.user=CustomUser.objects.create_user(username=code,
                                                                    first_name=first_name,
                                                                    last_name=last_name,
                                password='password3', email=email,
                                user_type=3)
        except:
            logging.getLogger("error_logger").error()
            messages.error(self, '{}'.format(ExaminerForm.errors))
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
        context['myFilter']=ExaminerFilter(queryset=Examiner.objects.all())
        #context['myFilter']=ExaminerFilter(self.request.GET, queryset=Examiner.objects.all())
        return context
         
    def post(self,request,*args, **kwargs):
        if request.method=="POST":
            Examiner.objects.filter(id__in=request.POST.getlist('id[]')).delete()
        return redirect('examiner-list')

def batchmailExaminer(request):
    if request.method=="POST":
        toMail=request.POST.getlist('id[]')
        maillist=[]
        for item in toMail:
            examiner=Examiner.objects.get(pk=item)
            maillist.append(examiner.email)
            
        try:
            if maillist:
                print("mail List :",maillist)
                send_mail(
                    'ECZ Examiner application approval',
                    'Hellow Examiner,Your application has been approved.Thank you',
                    'microvich@zohomail.com',
                    maillist,
                    fail_silently=False,
                )
            else:
                logging.getLogger("error_logger").error()
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            
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
            try:
                if examiner.availability==True: 
                    examiner.approved=True
                    examiner.save()
                else:
                    messages.warning(request,"Examiner whose status is unavailable will not be approved")
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
          
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
    
class SessionCreate(ListView):
    model=Session
    context_object_name='sessions'
    template_name='sessions/sessions.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        sessions=Session.objects.all()
        for item in sessions:
            if item.end_date<= date.today():
                item.active=False
                item.save()
        context['sessions']=Session.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        name=self.request.POST.get('session_name')
        start=self.request.POST.get('start_date')
        end=self.request.POST.get('end_date')
        session=Session.objects.create(name=name,start_date=start,end_date=end)
        session.save()
        context={
            'sessions':Session.objects.all()
        }
        messages.success(request,"Session Created")
        return redirect('sessions-all')
        #return render(request,'sessions/sessions.html',context)

def batchSessionDelete(request):
    if request.method=="POST":
        Session.objects.filter(id__in=request.POST.getlist('id[]')).delete()
    messages.success(request,"Deleted")   
    return redirect('sessions-all')


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

def examiners_per_subject(request):
    subjects=Subject.objects.all()
    examiners=Examiner.objects.all()
    subject_count=subjects.count()
    context={
        'subjects':subjects,
        'examiners':examiners,
        'subject_count':subject_count,
    }
    
    return render(request,'Subject/examiners_per_subject.html',context)

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


#Upload Examiner (while creating Users)
def upload_csv(request): 
    data = {}
    if "GET" == request.method:
        return render(request, "registration/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("examiner_upload_csv"))
    # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("examiner_upload_csv"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        lines=lines[1:len(lines)-1]
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            print("=======Line: ",line)
            fields = line.split(",")
            data_dict = {}
            data_dict["first_name"] =fields[1]  # field=uploaded file column
            data_dict["middle_name"] = fields[2]
            data_dict["last_name"] = fields[3]
            sub=Subject.objects.get(subjectName=fields[4])
            data_dict["subject"] = sub.id   # field=uploaded file column
            data_dict["email"] = fields[5]
            positionData=Position.objects.get(name=fields[6])
            data_dict["position"] =positionData.id
           # data_dict["approved"] = True
            #data_dict["availability"] = True 
            
            try: 
                form = ExaminerUploadForm(data_dict)
                print("data_dict:",data_dict)
                if form.is_valid():
                    form.save()
                    td=str(date.today().year)
                    code=td[-2:]+'-'+form.instance.subject.subjectCode+str(form.instance.pk)
                    print("CODE:",code)
                    form.instance.ExaminerCode=code
                    first_name=form.instance.first_name
                    last_name=form.instance.last_name
                    email=form.instance.email
                    form.instance.availability=True
                    form.instance.user=CustomUser.objects.create_user(username=code,first_name=first_name,
                                                   last_name=last_name,
                                                    email=email,
                                                    user_type=3,
                                                    password='password3')
                    form.save()
                    messages.success(request,"successifully uploaded examiners")
                else:

                    logging.getLogger("error_logger").error(
                       form.errors.as_json())
                    messages.error(request, '{}'.format(form.errors,line))
                   
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("examiner_upload_csv"))

   