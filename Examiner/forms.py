from dataclasses import field, fields
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Examiner,EAD,CustomUser,Person,City,Invitation ,districtcsv,Subject,Bank,BankBranch,Staff,comment

class ExaminerForm(forms.ModelForm):
    class Meta:
        model=Examiner 
        #fields='__all__'
        fields=('middle_name','last_name','first_name','gender','subject','position','Address','province','district',
                'AccountDetails','NRC','TPIN','cell_Number','email','availability','bank','branch')
        def clean(self):
 
            # data from the form is fetched using super function
            super(ExaminerForm, self).clean()
            
            # extract the username and text field from the data
            first_name = self.cleaned_data.get('first_name')
            email = self.cleaned_data.get('email')
    
            # conditions to be met for the username length
            if len(first_name) < 5:
                self._errors['username'] = self.error_class([
                    'Minimum 5 characters required'])
            if len(email) <10:
                self._errors['text'] = self.error_class([
                    'Post Should Contain a minimum of 10 characters'])
    
            # return any errors if found
            return self.cleaned_data
        
        widgets = {
            'middle_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Middle Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'gender':forms.Select(attrs={'class':'form-control '}),
            'subject': forms.Select(attrs={'class':'form-control '}),
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
        }



class EADForm(forms.ModelForm):
    class Meta:
        model=EAD
        fields=('first_name','last_name','gender','UserName','middle_name','bank','branch','AccountDetails','NRC','TPIN','cell_Number','email','Address','province','district')
        widgets = {
            'UserName':forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            'bank': forms.Select(attrs={'class':'form-control '}),
            'branch': forms.Select(attrs={'class':'form-control '}),
            'AccountDetails':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'NRC':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'TPIN':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'cell_Number':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
            'Address':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}), 
            'province':forms.Select(attrs={'class':'form-control '}),
            'gender':forms.Select(attrs={'class':'form-control '}),
            'district':forms.Select(attrs={'class':'form-control '}),
            
        }
    
#===========================================
class PersonCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


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
        fields=('first_name','last_name','gender','UserName','middle_name','bank','branch','AccountDetails','NRC','TPIN','cell_Number','email','Address','province','district')
        widgets = {
            'UserName':forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            'bank': forms.Select(attrs={'class':'form-control '}),
            'branch': forms.Select(attrs={'class':'form-control '}),
            'gender':forms.Select(attrs={'class':'form-control '}),
            'AccountDetails':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'NRC':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'TPIN':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'cell_Number':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@abc.abc'}),
            'Address':forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}), 
            'province':forms.Select(attrs={'class':'form-control '}),
            'district':forms.Select(attrs={'class':'form-control '}),
            
        }
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields=('first_name','last_name','email','user_type','password') 
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'lastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'password'}),
            'user_type': forms.Select(attrs={'class':'form-control '}),  
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

#<input type="password" name="new_password1" autocomplete="new-password" required="" id="id_new_password1">


