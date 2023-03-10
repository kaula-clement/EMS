
from django.urls import path
from . import views,EADViews,ExaminerViews,StaffViews,AuthView,AdminViews
from .views import Home,BankListView
from django.contrib.auth.views import LogoutView
from . EADViews import NotificationList,SubjectCreateView,SubjectListView,SubjectUpdateView,SubjectDeleteView,EADCreateView,EADListView,EADDeleteView,EADUpdateView,InviteView,ExaminerCreate,ExaminerList,ExaminerDetail,ExaminerUpdate,ExaminerDelete,EADUpdate
from . AuthView import CustomGroupList,CustomUserList,CustomUserUpdate,CustomLoginView
from .StaffViews import StaffExaminerList


#app_name='Examiner'

urlpatterns = [
   
   path('',CustomLoginView.as_view(),name='home'), #Home / Landing page
   
   #AUTH and Registration urls
   path('login/',CustomLoginView.as_view(),name='login'),
   path('register/',views.Registerpage.as_view(),name='register'),
   path('register-confirm/',views.confirmRegDetails,name='register-confirm'),
   
   path('logout/',LogoutView.as_view(next_page='login'),name='logout'), 
   path('update-user/<int:pk>/',AuthView.CustomUserUpdate,name='update-user'),
   path('group-list',CustomGroupList.as_view(),name='group-list'),
   
   path('new-user/',AuthView.createUserView,name='add-user'),
   path('delete-user/<str:pk>',AuthView.deleteCustomUser,name='delete-user'),
   
   
   #===================================ADMIN UTILS======================
   path('audit-logs/',AdminViews.logEntries,name='log-entries'),
   
   #====================================EAD Menu
   path('ead-home/',EADViews.EADHome,name='ead-home'),
   path('examiner/<int:pk>',ExaminerDetail.as_view(),name='examiner-details'),
   path('examiner/requests',EADViews.examinerRequests,name='examiner-requests'),
   path('examiner-edit/<int:pk>',ExaminerUpdate.as_view(),name='examiner-edit'),
   path('confirmed-examiners-list',EADViews.confirmedExaminers,name='confirmed-list'),
   path('examiner-delete/<int:pk>',ExaminerDelete.as_view(),name='examiner-delete'),
   path('create/',ExaminerCreate.as_view(),name='add-examiner'),
    
   path('list/',ExaminerList.as_view(),name='examiner-list'),
   path('invite-examiner/',InviteView.as_view(),name='invite'),
   path('add-ead/',EADCreateView.as_view(),name='ead-create'),
   path('ead-list/',EADListView.as_view(),name='ead-list'),
   
   path('maillist/',EADViews.mailList,name='mail-list'),
   path('batchmail/',EADViews.batchmailExaminer,name='batch-mail'),
   path('ead/<int:pk>',EADListView.as_view(),name='ead-details'),
   path('ead-delete/<int:pk>',EADDeleteView.as_view(),name='ead-delete'),
   path('ead/<int:pk>/',EADUpdateView.as_view(),name='update-ead'),
   path('updated-profile/',EADViews.updateprofilesave,name='profile-save'),
   path('updateprofile/<str:pk>',AuthView.updateprofile,name='updateprofile'),
   path('password-update',AuthView.updatepassword,name='updatepassword'),
   path('staff/create',StaffViews.StaffCreate.as_view(),name='staff-create'),
   path('staff/list',StaffViews.StaffListView.as_view(),name='staff-list'),
   path('stationadmins/',StaffViews.stationAdminUpdate,name='station-admin-list'),
   path('reports/',EADViews.reports,name='reports'),
   
   
   path('create-staff',EADViews.ECZStaffCreateView.as_view(),name='ECZStaff-create'),
   
   path('Sessions-all/',EADViews.SessionCreate.as_view(), name='sessions-all'),
   path('Session/update/<int:pk>',EADViews.SessionUpdate,name='session-update'),
   path('batch-session-delete/',EADViews.batchSessionDelete,name='batch-session-delete'),
   
   path('subjects/marking-center/',EADViews.selectMarkingVenue,name='marking-center'),
   
   #======================================Staff Menu
   path('Staff-home/',StaffViews.StaffHome,name='staff-home'), 
   path('staff/examiners/',StaffExaminerList.as_view(),name='staff-examiner-list'),  
   
   path('Examiner/attendance/',StaffViews.attendanceView,name='attendance'),
   path('Examiner/take-attendance/',StaffViews.takeattendance,name='take-attendance'),
   path('Examiner/present/<int:pk>',StaffViews.present,name='present-link'),
   path('Examiner/absent/<int:pk>',StaffViews.absent,name='absent-link'),
   path('reset/attendance/<int:pk>',StaffViews.resetAttendance,name="reset-link"),
   path('delete-schedule-data/',StaffViews.deletescheduledata,name="delete-schedule-data"),
   
   path('Examiner/schedule/',StaffViews.schedule,name='schedule'),
   path('schedule/',StaffViews.ScheduleTableList.as_view(), name='schedule_table'),
   path('schedule-delete/',StaffViews.deletescheduledata, name='delete-data'),
   path('paycalc/',StaffViews.calculatePay, name='calculate-pay'),
   path('Upload/stations/',StaffViews.upload_stations_csv,name='upload_stations'),
   path('update/examiner/<int:pk>',StaffViews.updateExaminer,name='update-examiner-SAD'),
   path('myexaminers/',StaffViews.myList,name='mylist'),
   
      
   #=====================================Examiner menu
   path('Examiner-home/',ExaminerViews.ExaminerHome,name='Examiner-home'),
   path('invite-response/<int:pk>',ExaminerViews.invitationResponse.as_view(),name='invite-response'),
   path('invite-approve/<inv_id>',ExaminerViews.invitation_approve,name='invite-approve'),
   path('invite-reject/<inv_id>',ExaminerViews.invitation_reject,name='invite-reject'),
   path('notifications/',ExaminerViews.NotificationList.as_view(),name='notifications-list'),
   path('download/invitation-letter',ExaminerViews.letter2pdf,name='download-letter'),
   path('comments/list',ExaminerViews.examinerComment,name='comments-list'),
   
   path('updatemyprofile/<str:pk>',ExaminerViews.examinerProfileUpdate,name='updatemyprofile'),
   path('updatemydetails/<str:pk>',ExaminerViews.examinerDetailsUpdate,name='updatemyDetails'),
   

   #=================================
   path('add-subject/',SubjectCreateView.as_view(),name='add-subject'),
   path('subject-list/',SubjectListView.as_view(),name='subject-list'),
   path('subject/<int:pk>',SubjectUpdateView.as_view(),name='subject-update'),
   path('subject-delete/<int:pk>',SubjectDeleteView.as_view(),name='subject-delete'),

   #===================================
   
   path('ajax/load-district/',views.load_district,name='load_districts'),

   #===========================UPLOADVIEWS=========

   path('upload-examiners/csv/', EADViews.upload_csv, name='examiner_upload_csv'),
   path('upload-districts/csv/',views.upload_district_csv, name='upload_district_csv'),
   
   path('upload-schedule-data',StaffViews.upload_schedule_csv, name='upload_schedule_csv'),

   #=========================================

    path('ajax/load-districts/', views.get_districts_ajax, name='load-districts'), # AJAX
    path('ajax/load-bank-branches/', views.get_bankbranch_ajax, name='load-bank-branches'), # AJAX
    path('get-papernumber-ajax/', views.get_papernumber_ajax, name="get_papernumber_ajax"),

    #path('upload-subjects/',views.uploadSubject,name='uploadSubject'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('export-csv/',views.export_csv,name='export-csv'), 
    path('export-excel/',views.export_excel,name='export-excel'),
    path('upload-subjects/',views.upload_subjects_csv,name="upload_subjects_csv"),
    
     
    path('users/',CustomUserList.as_view(),name='userlist'),


    path('get-topics-ajax/', views.get_topics_ajax, name="get_topics_ajax"),
    
    
       
    #====================banks================
    path('banks/linst/',BankListView.as_view(),name='bank-list'),    
    path('emails/',views.sendmail,name='send-email'),
   #============Analytics
    path('Subject/Examiner/bord',EADViews.examiners_per_subject,name='subject-bord'),
   ] 

#===========TO DELETE==============
# name='send-email' and co views
#,name='ECZStaff-create/list,/..