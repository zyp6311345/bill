from django.shortcuts import redirect


def is_login(view_func):
    """用于验证是否记住登录的功能"""
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('is_login'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return wrapper