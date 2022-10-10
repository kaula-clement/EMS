from django .http import HttpResponse
from django .shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
            
        else:
            return redirect('login')

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user=request.user.user_type
            modulename = view_func.__module__
            if modulename=='Examiner.EADViews':
                print("+++++++=======================================")
                print("Wrapper well set:",user)
                print(modulename)
            return view_func(request, *args, **kwargs)

        return wrapper_func
    return decorator