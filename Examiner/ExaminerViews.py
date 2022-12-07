import datetime
from unittest import result
from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging
from .models import CustomUser, Examiner,Invitation , comment
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from . forms import CommentForm,UpdateUserForm,ExaminerForm
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
import tempfile


#======================================

class CustomLoginView(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('home')
        #return reverse_lazy('examiner-list')

@login_required()
def ExaminerHome(request):
    examiner_obj=Examiner.objects.get(ExaminerCode=request.user.username)
    notifications=Invitation.objects.filter(toAddress=request.user.id)
    T_nots=notifications.count()
    context={'notifications':notifications,
             'T_nots':T_nots,
             'examiner':examiner_obj,
             }
    return render(request, 'Examiner/Examiner_home.html',context)

@login_required()
def examinerProfileUpdate(request,pk):
    user=request.user
    form=UpdateUserForm(instance=user)
    context={
        'form':form,
    }
    if request.method=="POST":
        form=UpdateUserForm(request.POST,instance=user)
        if form.is_valid():
            examiner=Examiner.objects.get(user=user)
            examiner.first_name=form.instance.first_name
            examiner.last_name=form.instance.last_name
            examiner.save()
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('login')
        else:
            logging.getLogger("error_logger").error(
                       form.errors.as_json())
            messages.error(request, '{}'.format(form.errors))
    return render(request,'Auth/update_profile.html',context)

@login_required()
def examinerDetailsUpdate(request,pk):
    user=request.user
    examiner=Examiner.objects.get(user=user)
    form=ExaminerForm(instance=examiner)
    context={
        "form":form,
    }
    if request.method=="POST":
        form=ExaminerForm(request.POST,instance=examiner)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('login')
        else:
            logging.getLogger("error_logger").error(
                       form.errors.as_json())
            messages.error(request, '{}'.format(form.errors))
    return render(request,'Examiner/updateDetails.html',context)
        
        

class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        examiner=Examiner.objects.get(user=self.request.user)
        context['letters']=Invitation.objects.filter(toAddress=examiner)
        
        return context



class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'

 
class ExaminerUpdate(LoginRequiredMixin,UpdateView):
    model=Examiner
    fields='__all__'
    success_url=reverse_lazy('examiner-list')

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

@csrf_exempt
def examinerComment(request):
    comments = comment.objects.all()
    examiners=Examiner.objects.filter(approved=True)
    context = {
        "examiners":examiners,
        "comments": comments
    }

    if request.method=="POST":
        exId = request.POST.get('id')
        msg = request.POST.get('msg')
        commentFrom=request.POST.get('user')
        try:
            comment.examiner=Examiner.objects.get(id=exId)
            comment.commentAuthor=CustomUser.objects.get(id=commentFrom)
            comment.msg = msg
            comment.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")
    
    return render(request, 'Examiner/comments.html', context)

@login_required()
def letter2pdf(request):
    pass
""" response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename=Examiners_invitation_letter'+str(datetime.now())+'.pdf'
    response['content-Transfer-Encoding']='binary'
    
    html_string= render_to_string('confirm_Invitation.html')
    html=HTML(string=html_string)
    result= html.write_pdf()
    
    with tempfile.TemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        
        output=open(output.name, 'rb')
        response.write(output.read())
    
    return response
"""