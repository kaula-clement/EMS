import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from requests import request
from .models import CustomUser,EAD,Examiner,Province,Staff,Bank,ECZStaff
from .forms import ChangePassword, EADForm, ExaminerForm, StaffForm, UserForm,ECZStaffForm,UpdateUserForm,UpdateExaminerUserForm
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user.user_type
        if user == 0:
            return reverse_lazy('ead-home')
        if user == 1:
            return reverse_lazy('ead-home')
        if user == 2:
            return reverse_lazy('staff-home')
        if user == 4:
            return reverse_lazy('staff-home')
         
        else:
            return reverse_lazy('Examiner-home')

class CustomGroupList(LoginRequiredMixin,ListView):
    model=Group
    context_object_name='groups'
    template_name ='EAD/Groups.html'

class CustomUserList(LoginRequiredMixin,ListView):
    model=CustomUser
    #context_object_name='staff_users'
    template_name='EAD/userList.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['staff_users']=CustomUser.objects.exclude(Q(user_type=3)|Q(is_superuser=True))
        context['examiner_users']=CustomUser.objects.filter(Q(user_type=3))
        return context

class CustomUserUpdate(LoginRequiredMixin,UpdateView):
    model=CustomUser
    form_class=UserForm
    context_object_name= 'User'
    template_name='EAD/userManager.html'
    success_url=reverse_lazy('userlist') 
   
@login_required() 
def CustomUserUpdate(request,pk):
    user=CustomUser.objects.get(id=pk)
    userT=user.user_type
    print("===========")
    print("TYPE",userT)
    form=UserForm(instance=user)
    context={
        'form':form,
    }
   # print("=======================================================")
    
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        usertype=request.POST.get('user_type')
        activity=request.POST.get('is_active')
        
        userT=user.user_type
        if user.user_type == '3':
            print("USER TYPE",3)
        try: 
            if usertype == '0':
                    user=CustomUser.objects.get(id=pk)
                   # print("=============in 0TH user type")
                    user.username=username
                    user.email=email
                    user.first_name=first_name
                    user.last_name=last_name
                    user.user_type=request.POST.get('user_type')
                    if activity=='on':
                        user.is_active=True
                    else:
                        user.is_active=False
                    user.is_admin=True
                    user.save()
                    if not user:
                        messages.error(request,'user update failed')
                        return redirect('userlist')

                    else:
                        messages.success(request, 'Admin user updated')
                        return redirect('userlist')
                    
            elif usertype == '1':
                form=EADForm(request.POST,instance=user)
            elif usertype == '2':
                form=StaffForm(request.POST,instance=user)
               # if form.is_valid():
                    #form.save()
                    #messages.success(request, 'Examier user updated')      
                    #examiner=Examiner.objects.get(user=user)
                    #examiner.email=email
                    #examiner.first_name=first_name
                    #examiner.last_name=last_name
                    #examiner.save()
                    #messages.success(request,"user update successiful ")
                    #return redirect('userlist')

                #else:
                  #  messages.error(request,'Examiner account update failed')
                   # return redirect('userlist')
               
            
            elif usertype == '4':
                form=ECZStaffForm(request.POST,instance=user)
            if form.instance.user_type == 3:
                form=UpdateExaminerUserForm(request.POST,instance=user)
                examiner=Examiner.objects.get(user=form.instance)
                examiner.first_name=form.instance.first_name
                examiner.last_name=form.instance.last_name
                examiner.email=form.instance.email
                examiner.save()
           
            if form.is_valid():
                    form.save()
                    messages.success(request,"user update successiful ")
                    return redirect('userlist')
            else:
                error=str(form.errors)
                messages.error(request,error)
        except Exception as e:
            messages.error(request, " user update failed "+repr(e))
            
    
    return render(request,'EAD/userManager.html',context)
 
@login_required()    
def deleteCustomUser(request,pk):
    user=CustomUser.objects.get(id=pk)
    print('USER ID:',user.username)
    if user:
        try:
            user.delete()
            messages.success(request,"User Deleted successifully")
        except Exception as e:
             messages.error(request, "Delete user failed "+repr(e))
            
    return redirect('userlist')
    
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
    
@login_required()
def createUserView(request):
    usertypes=((0, "ADMIN"),(1, "EAD"), (2, "FAD"),(4,"Station-Admin"))
    form=UserForm()
    context={
        'form':form,
        'usertypes':usertypes,
    }
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        user_type=request.POST.get('user_type')
        
        try:
            
            if user_type == '0':
                    user=CustomUser.objects.create_user(username=username,email=email,password='password3',
                      first_name=first_name,last_name=last_name,user_type=user_type,is_active=True,is_admin=True)
                    if not user:
                        messages.error(request,'user creation failed')

                    else:
                        messages.success(request, 'Admin user created')
                        return redirect('userlist')
                    
            elif user_type == '1':
                form=EADForm(request.POST)
            elif user_type == '2':
                form=StaffForm(request.POST)
            elif user_type == '3':
                pass
            elif user_type == '4':
                form=ECZStaffForm(request.POST)

            
            if form.is_valid():
                    form.save()
                    messages.success(request,"added user ")
                    return redirect('userlist')
            else:
                error=str(form.errors)
                messages.error(request,error)
        except Exception as e:
            messages.error(request, "Add user failed "+repr(e))
            
        #user.save()
        
    return render(request,'registration/new_user.html',context)

@login_required()  
def updateprofile(request,pk): 
    if request.user.user_type==0:
        user_id=request.user.id
        User=CustomUser.objects.get(id=user_id)
        form=EADForm(instance=User)
    if request.user.user_type==1:
        User=EAD.objects.get(user=pk)
        form=EADForm(instance=User)
    elif request.user.user_type==2:
        User=Staff.objects.get(user=pk)
        form=StaffForm(instance=User)
    elif request.user.user_type==4:
        User=ECZStaff.objects.get(user=pk)
        form=ECZStaffForm(instance=User)
    elif request.user.user_type==3:
        User=Examiner.objects.get(user=pk)
        #form=ExaminerForm(instance=User)
        form=UpdateUserForm(instance=User)
    #print("============EAD:",User)
    provinces=Province.objects.all()
    
    context={
        'form':form,
        'provinces':provinces,
            }
    
    if request.method=="POST":
        if request.user.user_type==0:
            user_id=request.user.id
            User=CustomUser.objects.get(id=user_id)
            form=UpdateUserForm(request.POST,instance=User)
        if request.user.user_type==1:
            User=EAD.objects.get(user=pk)
            form=EADForm(request.POST,instance=User)
        elif request.user.user_type==2:
            User=Staff.objects.get(user=pk)
            form=StaffForm(request.POST,instance=User)
        elif request.user.user_type==4:
            User=ECZStaff.objects.get(user=pk)
            form=ECZStaffForm(request.POST,instance=User)
        elif request.user.user_type==3:
            User=Examiner.objects.get(user=pk)
            #form=UserForm(request.POST,instance=User)
            form=ExaminerForm(request.POST,instance=User)
            
        if form.is_valid(): 
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('login')
        else:
            logging.getLogger("error_logger").error(
                       form.errors.as_json())
            messages.error(request, '{}'.format(form.errors))
            #return HttpResponse("profile Update failed")
        
    return render(request,'EAD/update_profile.html',context)


@login_required()
def updatepassword(request):
    form=ChangePassword(request.user)
    context={
        'form':form,
    }  
    if request.method=='POST':
        form=ChangePassword(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('updateprofile' ,pk=request.user.id)
        else:
            messages.error(request, '{}'.format(form.errors))
            return render(request,'EAD/password_change.html',context)
            
    return render(request,'EAD/password_change.html',context)
        
  