from django import forms
from .models import Examiner,EAD,District,Province,Person,City,Invitation

class ExaminerForm(forms.ModelForm):
    class Meta:
        model=Examiner 
        fields=('country','city','name','subject','position','Address','province','district',
                'AccountDetails','NRC','TPIN','cell_Number','email')

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
       
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'subject': forms.Select(attrs={'class':'form-control'}),
            'position': forms.Select(attrs={'class':'form-control','placeholder':'Select Position'}),
            'Address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'province': forms.Select(attrs={'class':'form-control','placeholder':'Provinve'}),
            'district': forms.Select(attrs={'class':'form-control','placeholder':'District'}),
            'AccountDetails': forms.TextInput(attrs={'class':'form-control','placeholder':'Account Details'}),
            'NRC': forms.TextInput(attrs={'class':'form-control','placeholder':'NRC Number'}),
            'TPIN': forms.TextInput(attrs={'class':'form-control','placeholder':'T Pin'}),
            'cell_Number': forms.TextInput(attrs={'class':'form-control','placeholder':'cell phone number'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email@..com'}),
        }

      #province id_province
      #district id_districts
      #




class EADForm(forms.ModelForm):
    class Meta:
        model=EAD
        fields=('firstName','LastName','UserName')
        widgets = {
            'firstName': forms.TextInput(attrs={'class':'form-control','placeholder':'firstName'}),
            'LastName': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'UserName': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            
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
        fields=('toAddress','title',)
        widgets = {
            'toAddress': forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Send To'}),
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
            
        }
