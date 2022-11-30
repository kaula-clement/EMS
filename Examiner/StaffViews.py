from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from django.db.models import Q
from .models import Examiner,Invitation,CustomUser,Staff,Bank,BankBranch,SchedulePay,Province,District,Payment,Attendance,ECZStaff,Subject
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StaffForm,ScheduleForm,StationForm

import logging
from django.contrib import messages

#======================================
@login_required()
def StaffHome(request): 
    if request.user.user_type == 4:
        user=ECZStaff.objects.get(username=request.user.username)
    elif request.user.user_type == 2:
        user=Staff.objects.get(username=request.user.username)
    print("User:",user.first_name)
    approved=Examiner.objects.filter(approved=True)
    examiners=Attendance.objects.filter(status=2)
    absent=Attendance.objects.filter(status=3)
    pending=Attendance.objects.filter(status=1)
    
    examiners_count=examiners.count()
    branches=BankBranch.objects.all
    scheduleTable=SchedulePay.objects.all()
    context={
            'examiners_count':examiners_count,
            'examiners':examiners,
          'branches':branches,
          'scheduleTable':scheduleTable,
          'approved':approved,
          'absent':absent,
          'pending':pending,
            }
    return render(request, 'Staff/Staff_home.html',context)


class StaffCreate(LoginRequiredMixin,CreateView):
    model=Staff
    form_class=StaffForm
    template_name='Staff/staff_form.html'
    success_url=reverse_lazy('staff-list')
    def form_valid(self, StaffForm):
        #pre save to get id
        super().form_valid(StaffForm) 
        #create user for the staff
        StaffForm.instance.user=CustomUser.objects.create_user(username=self.request.POST.get('UserName'),
                                                               first_name=self.request.POST.get('first_name'),
                                                               last_name=self.request.POST.get('last_name'),
                            password='password3', email='MicroVich.1@abc.com',
                            user_type=2)
            #return a valid form
        print("User Staff created:")
        print("Usename: ",)
        return super(StaffForm,self).form_valid(StaffForm)

class StaffListView(ListView):
    model=Staff
    template_name='EAD/Stafflist.html'
    context_object_name='staffs'
 
class StaffExaminerList(LoginRequiredMixin,ListView):
    model=Examiner
    queryset= Examiner.objects.filter(approved=True)
    template_name='Staff/Examiner_list.html'
    context_object_name='examiners' 

def attendanceView(request):
    user=ECZStaff.objects.get(username=request.user.username)
    examiners=Examiner.objects.filter(approved=True,
                                        subject=user.subject,
                                        paper=user.paper)
    for item in examiners:
        attendance=Attendance.objects.get_or_create(examiner=item)
        attendance[0].save()
    attendance=Attendance.objects.all()
    context={
        'attendance':attendance
    }
    messages.success(request,"Updated examiner list Successifuly")
    return redirect('take-attendance')


@login_required()
def takeattendance(request):
    #user=ECZStaff.objects.get(username=request.user.username)
    subjects=Subject.objects.all()
    examiners=Examiner.objects.filter(approved=0)#,
                                       # subject=user.subject,
                                        #paper=user.paper)
    attendance=Attendance.objects.filter(examiner__in=examiners)
    
    if request.method=="POST":
        subcode=request.POST.get('subject')    
        paper_number=request.POST.get('paper')
        
        examiners=Examiner.objects.filter(Q(subject=subcode)&
                                          Q(paper=paper_number))
        attendance=Attendance.objects.filter(examiner__in=examiners)
       # redirect('take-attendance')
    context={
        'subjects':subjects,
        'attendance':attendance,
        'examiners':examiners,
    }
    return render(request,"Staff/takeattendancesheet.html",context)
def present(request,pk):
    attendance=Attendance.objects.get(id=pk)
    attendance.status=2
    attendance.save()
    return redirect('take-attendance')

def absent(request,pk):
    attendance=Attendance.objects.get(id=pk)
    attendance.status=3
    attendance.save()
    return redirect('take-attendance')    
    
class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'


class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'
    
class ScheduleTableList(LoginRequiredMixin,ListView):
    model= SchedulePay
    context_object_name='schedule'
    template_name='Staff/ScheduleTable.html'

@login_required()
def schedule(request):
    present_examiners=Attendance.objects.filter(status=2)
    examiners=Examiner.objects.filter(attendance_examiner__in=present_examiners)
    ratePerNight=1000
    for item in examiners:
        
        fromStation=item.district
        toStation=item.to_province
        payment=Payment.objects.get_or_create(examiner=item)
       # print("==================")
        #print("Payment:",payment[0].transport)
        #print("Name:",item.first_name)
        #print("Province:",item.province)
        #print("From",fromStation)
        #print("To",toStation)
        try: 
            #print("Pay1:",payment[0].transport)
            nights=SchedulePay.objects.get(FromDistrict=fromStation)
            #print("Night Row",nights)
            nights=getattr(nights,toStation)
            #print("Nights2",nights)
            payment[0].transport=int(nights)*ratePerNight
            payment[0].save()
            #print("Pay:",payment[0].transport)
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
        
    context={
        'examiners':examiners,
        'payments':Payment.objects.all(),
    }
    return render(request,'Staff/Schedule.html',context)
    
    
def calculatePay(request):
    pay=0
    provinces=Province.objects.all()
    districts=District.objects.all()
    paydata=SchedulePay.objects.all()
    Stations=['LUSAKA','COPPERBELT','MONZE','KAPIRI','LIVINGSTONE',
                'CHOMA','MWANDI','LUNTE','MWENSE','KASENENGWA','CHISAMBA','CHIBOMBO',]
    context={
        'paydata':paydata,
        'provinces':provinces,
        'Stations':Stations,
        'districts':districts
    }
    
    if request.method=="POST":
        station=request.POST.get('station')
        fromdistrict=request.POST.get('district')
        payobj=SchedulePay.objects.get(FromDistrict_id=fromdistrict)
        nights=getattr(payobj,station)
        rate=1000
        pay=rate*nights
        context['pay']=pay
        return render(request,'Staff/calculatepay.html',context)
    
    return render(request,'Staff/calculatepay.html',context)
    


#Upload SCHEDULE DATA
@login_required()
def upload_schedule_csv(request): 
    data = {}
    if "GET" == request.method:
        return render(request, "Staff/upload_schedule_csv .html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_schedule_csv"))
    # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_schedule_csv"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        lines=lines[1:len(lines)-1]
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            print("=======Line: ",line)
            fields = line.split(",")
            data_dict = {}
            
            data_dict["FromDistrict"] =fields[1] 
            data_dict["LUSAKA"] = fields[2]
            data_dict["COPPERBELT"] = fields[3]
            data_dict["MONZE"] = fields[4]
            data_dict["KAPIRI"] = fields[5]
            data_dict["LIVINGSTONE"] = fields[6]
            data_dict["CHOMA"] = fields[7]
            data_dict["MWANDI"] = fields[8]
            data_dict["LUNTE"] = fields[9]
            data_dict["MWENSE"] = fields[10]
            data_dict["KASENENGWA"] = fields[11]
            data_dict["CHISAMBA"] = fields[12]
            data_dict["CHIBOMBO"] = fields[13]
            
            
            try : 
                form = ScheduleForm(data_dict)
                print("data_dict:",data_dict)
                if form.is_valid():
                    form.save()
                    messages.success(request,"successifully uploaded ")
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

    return HttpResponseRedirect(reverse("upload_schedule_csv"))

#Upload Stations
def upload_stations_csv(request): 
    data = {}
    if "GET" == request.method:
        return render(request, "Staff/upload_stations.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_stations"))
    # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_stations"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        lines=lines[1:len(lines)-1]
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            print("=======Line: ",line)
            fields = line.split(",")
            data_dict = {}
            
            data_dict["province"] =fields[0]  # field=uploaded file column
            data_dict["name"] = fields[1]
            
            try: 
                form = StationForm(data_dict)
                print("data_dict:",data_dict)
                if form.is_valid():
                    form.save()
                    messages.success(request,"uploaded record")
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

    return HttpResponseRedirect(reverse("upload_stations"))