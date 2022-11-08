import imp
import django_filters
from .models import Examiner,Staff,EAD,Subject,Invitation

class ExaminerFilter(django_filters.FilterSet):
    class Meta:
        model:Examiner
        fields='__all__'
        #fields=('middle_name','last_name','first_name','gender','subject','position','Address','province','district',
        #        'AccountDetails','NRC','TPIN','cell_Number','email','availability','bank','branch')