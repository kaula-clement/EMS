from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from .models import Examiner,Invitation,CustomUser,Staff,Bank,BankBranch,SchedulePay,Province,District
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StaffForm,ScheduleForm

import logging
from django.contrib import messages

#======================================

def StaffHome(request): 
    examiners=Examiner.objects.all()
    examiners_count=examiners.count()
    #branches=BankBranch.objects.all()
    available_examiners=examiners.filter(availability=True).count()
    context={
            'examiners_count':examiners_count,
            'available_examiners':available_examiners,
          #  'branches':branches
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
    
    
    
    
class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'


class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'
    
class ScheduleTableList(ListView):
    model= SchedulePay
    context_object_name='schedule'
    template_name='Staff/ScheduleTable.html'
    
    
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
    


#Upload SCHEDULE
def upload_schedule_csv(request): 
    data = {}
    if "GET" == request.method:
        return render(request, "Staff/upload_schedule_csv.html", data)
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
            
            data_dict["FromDistrict"] =fields[0]  # field=uploaded file column
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
            
            
            try: 
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