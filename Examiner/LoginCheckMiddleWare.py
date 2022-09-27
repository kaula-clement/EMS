from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "Examiner.EADViews":
                    pass
                elif modulename == "Examiner.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("home")
            
            elif user.user_type == "2":
                if modulename == "Examiner.StaffViews":
                    pass
                elif modulename == "Examiner.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")
            
            elif user.user_type == "3":
                if modulename == "Examiner.StudentViews":
                    pass
                elif modulename == "Examiner.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("student_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse("login"):
                pass
            else:
                return redirect("login")
