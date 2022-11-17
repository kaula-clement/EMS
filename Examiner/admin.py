from django.contrib import admin
from .models import Examiner,Subject,Position,Invitation,Province,District,EAD,CustomUser,Bank,BankBranch,Staff


class ExaminerAdmin(admin.ModelAdmin):
    fields=('email','first_name','last_name','middle_name','province','district','subject','position',)
    list_display=('user','email','province','district','ExaminerCode','id','subject','position','first_name','last_name','middle_name',)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('username','email','user_type','is_active')

class SubjectAdmin(admin.ModelAdmin):
    list_display=('id','subjectCode','subjectName')

class PositionAdmin(admin.ModelAdmin):
    list_display=('id','name')
    
class StaffAdmin(admin.ModelAdmin):
    fields=('first_name','UserName')
    list_display=('id','first_name','UserName')

class InvitationAdmin(admin.ModelAdmin):
    list_display=('title','StatusConfirm')

admin.site.register(Examiner,ExaminerAdmin)

admin.site.register(Subject,SubjectAdmin)

admin.site.register(Position,PositionAdmin)

admin.site.register(Invitation,InvitationAdmin)

admin.site.site_header='Examinations Council of zambia'

admin.site.register(Province)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(District)
admin.site.register(EAD)

admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(Staff,StaffAdmin)