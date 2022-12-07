from dataclasses import field, fields
from django import forms
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from .models import Examiner,EAD,CustomUser,Invitation ,districtcsv,Subject,Bank,BankBranch,Staff,comment,District,SchedulePay,Session,Station ,ECZStaff,Paper

class ExaminerUploadForm(forms.ModelForm):
    class Meta:
        model=Examiner
        fields=('middle_name','last_name','first_name','position','email','subject','paper',)
    
class ExaminerUpdateForm(forms.ModelForm):
    class Meta:
        model=Examiner
        fields=('middle_name','last_name','first_name','gender','subject','paper','position','Address','province','district',
                'AccountDetails','NRC','TPIN','cell_Number','email','bank','branch',)
        widgets = {
        'middle_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Middle Name'}),
        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
        'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
        'gender':forms.Select(attrs={'class':'form-control '}),
        'subject': forms.Select(attrs={'class':'form-control '}),
        'paper': forms.Select(attrs={'class':'form-control '}),
        'position': forms.Select(attrs={'class':'form-control','placeholder':'Select Position'}),
        'Address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
        'province': forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
        'district': forms.Select(attrs={'class':'form-control','placeholder':'District'}),
        'AccountDetails': forms.TextInput(attrs={'class':'form-control','placeholder':'Account Number'}),
        'NRC': forms.TextInput(attrs={'class':'form-control','placeholder':'NRC Number'}),
        'TPIN': forms.TextInput(attrs={'class':'form-control','placeholder':'T Pin'}),
        'cell_Number': forms.TextInput(attrs={'class':'form-control','placeholder':'cell phone number'}),
        'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
        'bank':forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
        'branch':forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
        
    }

class ExaminerForm(forms.ModelForm):
    class Meta:
        model=Examiner 
        fields=('middle_name','last_name','first_name','gender','subject','paper','position','Address','province','district',
                'AccountDetails','NRC','TPIN','cell_Number','email','availability','bank','branch','session',)
        
        widgets = {
            'middle_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Middle Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'gender':forms.Select(attrs={'class':'form-control '}),
            'subject': forms.Select(attrs={'class':'form-control '}),
            'paper': forms.Select(attrs={'class':'form-control '}),
            'position': forms.Select(attrs={'class':'form-control','placeholder':'Select Position'}),
            'Address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'province': forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
            'district': forms.Select(attrs={'class':'form-control','placeholder':'District'}),
            'AccountDetails': forms.TextInput(attrs={'class':'form-control','placeholder':'Account Number'}),
            'NRC': forms.TextInput(attrs={'class':'form-control','placeholder':'NRC Number'}),
            'TPIN': forms.TextInput(attrs={'class':'form-control','placeholder':'T Pin'}),
            'cell_Number': forms.TextInput(attrs={'class':'form-control','placeholder':'cell phone number'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
            'bank':forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
            'branch':forms.Select(attrs={'class':'form-control','placeholder':'Province'}),
            
            'approved':forms.CheckboxInput(attrs={'class':'largerCheckbox'}),
            'availability':forms.CheckboxInput(attrs={'class':'largerCheckbox'}),
            'session':forms.Select(attrs={'class':'form-control'}),
            
        }
    def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
            self.fields['session'].queryset = Session.objects.filter(active=True)



class EADForm(forms.ModelForm):
    class Meta:
        model=EAD
        fields=('username','first_name','last_name','email',)
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
            
        }
    
#===========================================


class InvitationForm(forms.ModelForm):
    class Meta:
        model=Invitation
        fields=('title','msg')
        widgets = {
            'msg': forms.TextInput(attrs={'class':'form-control','placeholder':'Message'}),
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            
        }


class DistForm(forms.ModelForm):
    class Meta:
        model=districtcsv
        fields=('code','name')

class SubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields=('subjectCode','subjectName','subjectDescription')
        
class PaperForm(forms.ModelForm):
    class Meta:
        model=Paper
        fields=('subject','paper_number','paper_name','paper_description',)
        
class BankBranchForm(forms.ModelForm):
    class Meta:
        model=BankBranch
        fields=('bank','name','sortcode')
        
class BankForm(forms.ModelForm):
    class Meta:
        model=Bank
        fields=('name',)
        
class StaffForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('username','first_name','last_name','email',)
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
            
        }
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields=('username','first_name','last_name','email','user_type','is_active') 
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'lastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'password'}),
            'user_type': forms.Select(attrs={'class':'form-control '}),  
            'is_active':forms.CheckboxInput(),
            
        } 

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email',)
        widgets = {
           # 'username': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'lastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            
        } 
class UpdateExaminerUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email','is_active')
        widgets = {
           # 'username': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'lastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            
        } 
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=('examiner','title','msg',)
        try:
            examiners = Examiner.objects.filter(approved=True)
            examiner_list = []
            for item in examiners:
                single_examiner = (item.id, item.first_name,item.last_name)
                examiner_list.append(single_examiner)
        except:
            examiner_list = []
        widgets = {
            'examiner': forms.Select(choices=examiner_list,attrs={'class':'form-control '}), 
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'msg': forms.Textarea(attrs={'class':'form-control','placeholder':'LastName'}),
             
        }


class ChangePassword(PasswordChangeForm):
   old_password = forms.CharField( max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
   new_password1 = forms.CharField( max_length=50, required="" , widget=forms.PasswordInput(attrs={"class":"form-control"}))
   new_password2 = forms.CharField( max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))



class DistrictForm(forms.ModelForm):
    class Meta:
        model=District
        fields='__all__'
        
class ScheduleForm(forms.ModelForm):
    class Meta:
        model=SchedulePay
        fields=('FromDistrict','LUSAKA','COPPERBELT','MONZE','KAPIRI','LIVINGSTONE',
                'CHOMA','MWANDI','LUNTE','MWENSE','KASENENGWA','CHISAMBA','CHIBOMBO',)
        
class StationForm(forms.ModelForm):
    class Meta:
        model=Station
        fields=('province','name')
       
class ECZStaffForm(forms.ModelForm):
    class Meta:
        model=ECZStaff
        fields=('username','first_name','last_name','email',)
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'lastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            
        } 
        
class SessionForm(forms.Form):
    name=forms.TextInput(attrs={'class':'form-control','placeholder':'Session Name'}),
    start_date=forms.DateInput()
    end_date=forms.DateInput()