from django.http import HttpResponseRedirect
from django.shortcuts import redirect,reverse
from .models import User
# d=dict()
# d['restaurant']='rdashboard'
# d['user']='udashboard'
# d['delivery']='ddashboard'


def unauthenticated_user(view_func):
	def wrapper_func(request,*args,**kwargs):
		if request.user.is_authenticated :
			return HttpResponseRedirect("dashboard")
		else:
			return view_func(request,*args,**kwargs)

	return wrapper_func
