from django.contrib import admin
from .models import Examiner,Subject,Position,Invitation,Province,District,EAD,Person,City,Country


class ExaminerAdmin(admin.ModelAdmin):
    fields=('email','name','province','district','subject','position','country','city')
    list_display=('user','email','province','district','ExaminerCode','id','subject','position','name','country','city')

class SubjectAdmin(admin.ModelAdmin):
    list_display=('id','subjectCode','subjectName')

class PositionAdmin(admin.ModelAdmin):
    list_display=('id','name')

class InvitationAdmin(admin.ModelAdmin):
    list_display=('title','StatusConfirm')

admin.site.register(Examiner,ExaminerAdmin)

admin.site.register(Subject,SubjectAdmin)

admin.site.register(Position,PositionAdmin)

admin.site.register(Invitation,InvitationAdmin)

admin.site.site_header='Examinations Council of zambia'

admin.site.register(Province)
admin.site.register(District)
admin.site.register(EAD)

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Person)