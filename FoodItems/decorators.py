from django.http import HttpResponse
from accounts.models import User

def only_customer(view_func):
    def wrapper_func(request , *args , **kwargs):
        if User.objects.get(username=request.user.username).type1 == "user":
            return view_func(request , *args , **kwargs)
        else:
            return HttpResponse("Not authorised to view this page")
    return wrapper_func


def only_restaurant(view_func):
    def wrapper_func(request , *args , **kwargs):
        if User.objects.get(username=request.user.username).type1 == "restaurant":
            return view_func(request , *args , **kwargs)
        else:
            return HttpResponse("Not authorised to view this page")
    return wrapper_func

def only_delivery(view_func):
    def wrapper_func(request , *args , **kwargs):
        if User.objects.get(username=request.user.username).type1 == "delivery":
            return view_func(request , *args , **kwargs)
        else:
            return HttpResponse("Not authorised to view this page")
    return wrapper_func
