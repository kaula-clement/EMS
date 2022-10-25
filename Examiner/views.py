from urllib import response

from requests import request
from .models import City,BankBranch,Bank,CustomUser
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Examiner, Invitation, Province, District,districtcsv
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

# ======================================
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BankBranchForm,ExaminerForm
# ======================================pdf
import csv
import xlwt
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import logging
from django.core.mail import send_mail
from datetime import date, datetime


class Registerpage(CreateView):
    model=Examiner
    form_class=ExaminerForm 
    template_name='registration/register.html'
    success_url=reverse_lazy('login')
    form=ExaminerForm
    def form_valid(self, ExaminerForm):
        td=str(date.today().year)
        #pre save to get id
        super().form_valid(ExaminerForm)
        #concatenate year(2digits)+[subject code]+ [id] to make code
        code=td[-2:]+'-'+ExaminerForm.instance.subject.subjectCode+str(self.object.id)
        #Examinercode is = concatenated code 
        ExaminerForm.instance.ExaminerCode=code
        #create user for the examiner
        first_name=ExaminerForm.instance.first_name
        last_name=ExaminerForm.instance.last_name
        user_email=ExaminerForm.instance.email
        ExaminerForm.instance.user=CustomUser.objects.create_user(username=code,
                                                                  first_name=first_name,
                                                                  last_name=last_name,
                            password='password3', email=user_email,
                            user_type=3)
                #return a valid form
        return super(Registerpage,self).form_valid(ExaminerForm)
   

@login_required()
def Home(request):
    # examiner_obj=Examiner.objects.get(ExaminerCode=request.user.user_id)
    notifications = Invitation.objects.filter(toAddress=request.user.id)
    T_nots = notifications.count()
    context = {
    }
    print("Im in the wrong view +++++++++++++++++++")
    if request.user.user_type == 1:
        return render(request, 'EAD/EAD_home.html', context)
    elif request.user.user_type == 3:
        return render(request, 'Examiner/Examiner_home.html', context)
    else:
        return HttpResponse("not valid user")


def load_district(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).all()
    print("==================================================")
    return render(request, 'registration/district_dropdown.html', {'districts': districts})


# AJAX
def get_districts_ajax(request):
    if request.method == "POST":
        province_id = request.POST['province_id']
        try:
            province = Province.objects.filter(id = province_id).first()
            print("Province with ID: ",province)
            districts = District.objects.filter(province = province)
        except Exception:
            pass
           # data['error_message'] = 'error'
           # return JsonResponse(data)
        return JsonResponse(list(districts.values('id', 'name')), safe = False) 
    
def get_bankbranch_ajax(request):
    if request.method == "POST":
        bank_id = request.POST['bank_id']
        try:
            bank = Bank.objects.filter(id = bank_id).first()
            print("Bank with ID: ",bank)
            branches = BankBranch.objects.filter(bank = bank)
        except Exception:
            pass
           # data['error_message'] = 'error'
           # return JsonResponse(data)
        return JsonResponse(list(branches.values('id', 'name')), safe = False)

# ===================================


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "Examiner/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
    # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_csv"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        data=districtcsv.objects.all()
        #print(data)
        for line in lines:
            print("=======Line: ",line)
            fields = line.split(",")
            data_dict = {}
            data_dict["bank"] =fields[6]  # field=uploaded file column
            data_dict["name"] = fields[0]
            data_dict["sortcode"] = fields[5]
            try: 
                form = BankBranchForm(data_dict)
                print("data_dict:",data_dict)
                if form.is_valid():
                    form.save()
                else:

                    logging.getLogger("error_logger").error(
                       form.errors.as_json())

            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))


from . models import Country, City, Person
from django.http import JsonResponse

def get_topics_ajax(request):
    if request.method == "POST":
        country_id = request.POST['country_id']
        try:
            country = Country.objects.filter(id = country_id).first()
            print("country with ID: ",country)
            cities = City.objects.filter(country = country)
        except Exception:
            pass
           # data['error_message'] = 'error'
           # return JsonResponse(data)
        return JsonResponse(list(cities.values('id', 'name')), safe = False)
    

    
class BankListView(ListView):
    model=BankBranch
    context_object_name='branches'
    template_name='registration/banks.html'

class BankCreateView(CreateView):
    model= BankBranch
    fields='__all__'
    context_object_name='branches'
    template_name='registration/banks.html'
    
    
def sendmail(request):
    send_mail('Testing mail',
              'JHellow user,This is a testing email',
              'kaulaclementb@gmail.com',
              ['rariyoj844@migonom.com'],
              fail_silently=False)
    return render(request,'registration/email_temp.html')

def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename=Examiners-schedule'+str(datetime.now())+'.csv'
    
    writer=csv.writer(response)
    writer.writerow(['ID','Examiner Number','First Name','Middle Name',
                     'Last Name','position','Subject','Province','District',
                     'Bank','Branch','Sort Code','Account Number'])
    examiners=Examiner.objects.filter(approved=True)
    for item in examiners:
        writer.writerow([item.id,item.ExaminerCode,item.first_name,item.middle_name,item.last_name,
                         item.position,item.subject,item.province,item.district,item.bank,
                         item.branch,item.branch.sortcode,
                         item.AccountDetails])
    return response

def export_excel(request):
    response=HttpResponse(content_type='ms-excel')
    response['Content-Disposition']='attachment;filename=Examiners-schedule'+str(datetime.now())+'.xls'
    
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Examiners')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    
    columns=['ID','Examiner Number','First Name','Middle Name',
                     'Last Name','position','Subject','Province','District',
                     'Bank','Branch','Sort Code','Account Number']
    
    for column_num in range(len(columns)):
        ws.write(row_num,column_num,columns[column_num],font_style)
    font_style=xlwt.XFStyle()
    
    examinerlist=[]
    print("=========================++++++++++++1111111")
    print(examinerlist)
    examiners=Examiner.objects.filter(approved=True)
    for item in examiners:
        examiner=(item.id,
            item.ExaminerCode,
            item.first_name,
            item.middle_name,
            item.last_name,
            str(item.position),
            str(item.subject),
            str(item.province),
            str(item.district),
            str(item.bank),
            str(item.branch),
            item.branch.sortcode,
            item.AccountDetails

        )
        examinerlist.append(examiner)
        
    rows=examinerlist
    print(rows)
    print("=========================+++++++++++++++2222")
    print(examinerlist)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
            
    wb.save(response)
    return response

            