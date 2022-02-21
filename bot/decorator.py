from django.shortcuts import redirect
from django.http import HttpResponse
def authenticated(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper
def allowed_users(allowed = []):
    def decorator(view):
        def wrapper(request,*args,**kwargs):
            user = request.user
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
                print('......................................',group)
                if group in allowed:
                    return view(request,*args,**kwargs)
                else:
                    return HttpResponse('<h1>Bu sahifaga kirish uchun szda ruhsat yo\'q</h1>')
        return wrapper
    return decorator