from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Examiner,Invitation , comment
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from . forms import CommentForm
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
def ExaminerHome(request):
    #examiner_obj=Examiner.objects.get(ExaminerCode=request.user.user_id)
    notifications=Invitation.objects.filter(toAddress=request.user.id)
    T_nots=notifications.count()
    context={'notifications':notifications,'T_nots':T_nots}
    return render(request, 'Examiner/Examiner_home.html',context)


class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'



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

"""  
class CommentsListView(ListView):
 
    model=comment

    context_object_name='comments'
    template_name='Examiner/comments.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['Examiners']=Examiner.objects.filter(approved=True)
        form=CommentForm
        context['form']=form
        return context
    def post(self,request,*args, **kwargs):
        if request.method=="POST":
            form=CommentForm()
            commentFor=request.POST.get('id')
            title=request.POST.get('title')
            text=request.POST.get('textmsg') 
            print("Printing Post Data:")
            print("Exam:",commentFor) 
            print("title:",title)
            print("Exam:",text)        
            #c =comment(examiner=commentFor,title=title,msg=text)
            
        return redirect('examiner-list')
    

 
class CommentCreateView(CreateView):


    form_set=CommentForm
    context_object_name='comment'
    success_url = reverse_lazy('comments-list')
"""