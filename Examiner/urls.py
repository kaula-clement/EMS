
from django.urls import path
from . import views,EADViews,ExaminerViews,StaffViews,AuthView
from .views import Home,BankListView
from django.contrib.auth.views import LogoutView
from . EADViews import NotificationList,SubjectCreateView,SubjectListView,SubjectUpdateView,SubjectDeleteView,EADCreateView,EADListView,EADDeleteView,EADUpdateView,InviteView,ExaminerCreate,ExaminerList,ExaminerDetail,ExaminerUpdate,ExaminerDelete,EADUpdate
from . AuthView import CustomGroupList,CustomUserList,CustomUserUpdate,CustomLoginView
from .StaffViews import StaffExaminerList


#app_name='Examiner'

urlpatterns = [
   
   path('',views.Home,name='home'), #Home / Landing page
   
   #AUTH and Registration urls
   path('login/',CustomLoginView.as_view(),name='login'),
   path('register/',views.Registerpage.as_view(),name='register'),
   path('logout/',LogoutView.as_view(next_page='login'),name='logout'), 
   path('update-user/<int:pk>/',CustomUserUpdate.as_view(),name='update-user'),
   path('group-list',CustomGroupList.as_view(),name='group-list'),
   
   
   
   #====================================EAD Menu
   path('ead-home/',EADViews.EADHome,name='ead-home'),
   path('examiner/<int:pk>',ExaminerDetail.as_view(),name='examiner-details'),
   path('examiner/requests',EADViews.examinerRequests,name='examiner-requests'),
   path('examiner-edit/<int:pk>',ExaminerUpdate.as_view(),name='examiner-edit'),
   path('examiner-delete/<int:pk>',ExaminerDelete.as_view(),name='examiner-delete'),
   path('create/',ExaminerCreate.as_view(),name='add-examiner'),
   path('list/',ExaminerList.as_view(),name='examiner-list'),
   path('invite-examiner/',InviteView.as_view(),name='invite'),
   path('add-ead/',EADCreateView.as_view(),name='ead-create'),
   path('ead-list/',EADListView.as_view(),name='ead-list'),
   path('ead/<int:pk>',EADListView.as_view(),name='ead-details'),
   path('ead-delete/<int:pk>',EADDeleteView.as_view(),name='ead-delete'),
   path('ead/<int:pk>/',EADUpdateView.as_view(),name='update-ead'),
   path('updated-profile/',EADViews.updateprofilesave,name='profile-save'),
   path('updateprofile/<str:pk>',AuthView.updateprofile,name='updateprofile'),
   path('password-update',AuthView.updatepassword,name='updatepassword'),
   #======================================Staff Menu
   path('Staff-home/',StaffViews.StaffHome,name='staff-home'),
   path('staff/examiners/',StaffExaminerList.as_view(),name='staff-examiner-list'),   
   
   
   
   
      
   #=====================================Examiner menu
   path('Examiner-home/',ExaminerViews.ExaminerHome,name='Examiner-home'),
   path('invite-response/<int:pk>',ExaminerViews.invitationResponse.as_view(),name='invite-response'),
   path('invite-approve/<inv_id>',ExaminerViews.invitation_approve,name='invite-approve'),
   path('invite-reject/<inv_id>',ExaminerViews.invitation_reject,name='invite-reject'),
   path('notifications/',NotificationList.as_view(),name='notifications-list'),
   
   path('comments/list',ExaminerViews.examinerComment,name='comments-list'),
   

   #=================================
   path('add-subject/',SubjectCreateView.as_view(),name='add-subject'),
   path('subject-list/',SubjectListView.as_view(),name='subject-list'),
   path('subject/<int:pk>',SubjectUpdateView.as_view(),name='subject-update'),
   path('subject-delete/<int:pk>',SubjectDeleteView.as_view(),name='subject-delete'),

   #===================================
   
   path('ajax/load-district/',views.load_district,name='load_districts'),

   #=========================================

  

   #=========================================

    path('ajax/load-districts/', views.get_districts_ajax, name='load-districts'), # AJAX
    path('ajax/load-bank-branches/', views.get_bankbranch_ajax, name='load-bank-branches'), # AJAX


    #path('upload-subjects/',views.uploadSubject,name='uploadSubject'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    
    path('users/',CustomUserList.as_view(),name='userlist'),


    path('get-topics-ajax/', views.get_topics_ajax, name="get_topics_ajax"),
    
    
    
    #====================banks================
    path('banks/linst/',BankListView.as_view(),name='bank-list'),
    
    path('emails/',views.sendmail,name='send-email'),


   ] 


"""
      # path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_staff/', HodViews.add_staff, name="add_staff"),
    path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', HodViews.delete_staff, name="delete_staff"),
    path('add_course/', HodViews.add_course, name="add_course"),
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
    path('manage_course/', HodViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"),
    path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"),
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session/', HodViews.add_session, name="add_session"),
    path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
    path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', HodViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', HodViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('staff_feedback_message/', HodViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', HodViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    path('student_leave_view/', HodViews.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', HodViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', HodViews.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', HodViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', HodViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', HodViews.staff_leave_reject, name="staff_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', HodViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    


    # URLS for Staff
   
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('save_attendance_data/', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('staff_update_attendance/', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates/', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', StaffViews.update_attendance_data, name="update_attendance_data"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
    path('staff_add_result/', StaffViews.staff_add_result, name="staff_add_result"),
    path('staff_add_result_save/', StaffViews.staff_add_result_save, name="staff_add_result_save"),

    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),

    """