from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Examiner,Invitation,Province,District
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ExaminerForm
#======================================
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#======================================pdf
from io import BytesIO
from django.http import FileResponse
from django.template.loader import get_template,render_to_string
from django.views import View
from xhtml2pdf import pisa
#from reportlab.pdfgen import canvas

#===================================

class CustomLoginView(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('home')
        #return reverse_lazy('examiner-list')

"""
class Home(LoginRequiredMixin,ListView):
    template_name='index.html'
    model=Examiner
    context_object_name='examiner'

    #to view only the examiner whose the user is loged 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['examiner',]= context['examiner'].filter(user=self.request.user)
        return context
 
"""
@login_required()
def Home(request):
    #examiner_obj=Examiner.objects.get(ExaminerCode=request.user.user_id)
    notifications=Invitation.objects.filter(toAddress=request.user.id)
    T_nots=notifications.count()
    context={'notifications':notifications,'T_nots':T_nots}
    return render(request, 'index.html',context)
'''    
def sendInvitation(request,UserID):
    fromUser=request.user
    toUser=User.objects.get(id=UserID)
'''

class ExaminerList(LoginRequiredMixin,ListView):
    model=Examiner
    context_object_name='examiners'


class ExaminerDetail(LoginRequiredMixin,DetailView):
    model=Examiner
    context_object_name='Examiner'

def ExaminerCreate(request):
    form=ExaminerForm()
    if request.method == 'POST':

        form = ExaminerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examiner-list')
    return render(request, 'Examiner/Examiner_form.html', {'form': form})





def load_district(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).all()
    print("==================================================")
    return render(request, 'registration/district_dropdown.html', {'districts': districts})


class ExaminerUpdate(LoginRequiredMixin,UpdateView):
    model=Examiner
    form_class=ExaminerForm
    success_url=reverse_lazy('examiner-list')

class ExaminerDelete(LoginRequiredMixin,DeleteView):
    model=Examiner
    context_object_name='Examiner'
    success_url=reverse_lazy('examiner-list')
#===========================================================

class NotificationList(LoginRequiredMixin,ListView):
    model=Invitation
    context_object_name='invitations'
    template_name='Examiner/notifications_list.html'

def invitationlist(request):
    toAddress=request.user.id
    invitations=Invitation.objects.filter(toAddress=toAddress).all()
    count=invitations.count()
    context={'invitations':invitations,
            'count':count}
    
    for item in invitations:
        print(item.id)
    return render(request, 'Examiner/notifications_list.html',context)


class invitationResponse(LoginRequiredMixin,UpdateView):
    model=Invitation
    template_name='confirm_Invitation.html'
    fields='__all__'
    context_object_name='invitation'
    success_url=reverse_lazy('home')

@login_required()
def invitation_approve(request, inv_id):
    invitation = Invitation.objects.get(id=inv_id)
    invitation.StatusConfirm = 1
    invitation.save()
    return redirect('home')

@login_required()
def invitation_reject(request, inv_id):
    invitation = Invitation.objects.get(id=inv_id)
    invitation.StatusConfirm = 2
    invitation.save()
    return redirect('home')
   
#===============================================================
def render_to_pdf(template_source,context_dict={}):
    template=get_template(template_source)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None
    buffer=io.BytesIO()


class GeneratePDF(View):
    def get(self,request,*args,**kwargs):
        data=Examiner.objects.get(id=10)
        open('templates/temp.html',"w").write(render_to_string('Examiner/Examiner_Detail.html',{'Examiner':Examiner}))
        pdf=render_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')


#================================================================
from .forms import PersonCreationForm
from .models import Person, City


def person_create_view(request):
    form = PersonCreationForm()
    if request.method == 'POST':
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_add')
    return render(request, 'persons/home.html', {'form': form})


def person_update_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonCreationForm(instance=person)
    if request.method == 'POST':
        form = PersonCreationForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_change', pk=pk)
    return render(request, 'persons/home.html', {'form': form})


# AJAX
def load_cities(request):
    country_id = request.GET.get('country_id')
    province_id = request.GET.get('province_id')

    cities = City.objects.filter(country_id=country_id).all()
    districts= District.objects.filter(province_id=province_id).all()

    return render(request, 'persons/city_dropdown_list_options.html', {'cities': cities,'districts':districts})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

