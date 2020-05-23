from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import User,Restaurant,DeliveryAgent,Customer
from django.urls import reverse
from .forms import SignUpForm,UserEditForm,RestaurantEditForm,DeliveryAgentEditForm
from .decorators import unauthenticated_user
from django.contrib import messages
# Create your views here.



def indexView(request):
	return render(request,'index.html')

@login_required
def dashboardView(request):

	type1=User.objects.get(username=request.user.username).type1
	if type1=='delivery':
		return redirect('/food/orders_available/')

	if type1=='restaurant':
		restaurant = Restaurant.objects.get(username_id=request.user.username)
		return render(request,'rdashboard.html',{'message':None,'restaurant':restaurant})

	else:
		return redirect('/fooditems/')


@unauthenticated_user
def registerView(request):
	print('registerView')
	if request.method == 'POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			print('formValid')
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			type1=request.POST["usertype"]
			print(username)
			user = authenticate(username=username, password=raw_password)

			login(request, user)
			sendDetails(request)
			if type1=='restaurant':
				initial=Restaurant.objects.create(username_id=User(username=username))
			elif type1=='user':
				initial=Customer.objects.create(username_id=User(username=username))
			else:
				initial=DeliveryAgent.objects.create(username_id=User(username=username))
			initial.save()


			return HttpResponseRedirect(reverse("dashboard"))
	else:
		form=SignUpForm()

	return render(request,'registration/register.html',{'form':form})


def sendDetails(request):
	print('sendDetails')
	u=User()
	u.username=request.POST["username"]
	u.fname=request.POST["fname"]
	u.lname=request.POST["lname"]
	u.phone=request.POST["phone"]
	u.email=request.POST["email"]
	u.type1=request.POST["usertype"]
	u.save()
	return

@unauthenticated_user
def loginView(request):
	context={}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			print(user.last_login)
			type1=User.objects.get(username=username).type1
			return HttpResponseRedirect(reverse("dashboard"))
		else:
			context["error"]="Provide valid credentials !!"
			return render(request,"registration/login.html",context)
	else:
		return render(request,'registration/login.html',context)

@login_required
def EditProfileView(request):

	type1=User.objects.get(username=request.user.username).type1
	if type1=='restaurant':
		res = Restaurant.objects.get(pk=request.user.username)
		if request.method=='POST':
			form = RestaurantEditForm(request.POST,request.FILES)
			print(res.name)
			if form.is_valid():
				form.save(commit=False)
				print('Form Valid')
				if request.POST.get('name')!= '' and request.POST.get('name')!=None:
					res.name=request.POST.get('name')

				if request.POST.get('Location')!='' and request.POST.get('Location')!=None:
					res.Location=request.POST.get('Location')

				if request.POST.get('startTime')!='' and request.POST.get('startTime')!=None:
					res.startTime=request.POST.get('startTime')

				if request.POST.get('closeTime')!='' and request.POST.get('closeTime')!=None:
					res.closeTime=request.POST.get('closeTime')

				if request.POST.get('cuisine')!='' and request.POST.get('cuisine')!=None:
					res.cuisine=request.POST.get('cuisine')

				if request.POST.get('pricePerHead')!='' and request.POST.get('pricePerHead')!=None:
					res.pricePerHead=request.POST.get('pricePerHead')

				if request.POST.get('contactNumber')!='' and request.POST.get('contactNumber')!=None:
					res.contactNumber=request.POST.get('contactNumber')

				if request.FILES.get('profile_pic') != '' and request.FILES.get('profile_pic') != None:
					name1,ext= request.FILES['profile_pic'].name.split('.')
					request.FILES['profile_pic'].name = str(request.user.username)+'.'+str(ext)
					print(request.FILES['profile_pic'].name)
					res.profile_pic = request.FILES.get('profile_pic')

				try:
					res.save()
					print('Saved')
					message={'message':"Update Successful"}
					return HttpResponseRedirect(reverse('dashboard'))
				except:
					pass

		else:
			form=RestaurantEditForm()

		return render(request,'profile.html',{'form':form,'type':type1})

	elif type1=='delivery':
		form=DeliveryAgentEditForm(request.POST)
		

		res=DeliveryAgent.objects.get(username=User(username=request.user.username))
		if form.is_valid():
			print('Form Valid')

			if (request.POST.get('status')== 'on'):
				res.status=True
			else:
				if res.status==False:
					res.status=False

			if request.POST.get('vehicleNumber')!='':
				res.vehicleNumber=request.POST.get('vehicleNumber')
			if request.POST.get('drivingLicense')!='':
				res.drivingLicense=request.POST.get('drivingLicense')
			if request.POST.get('rating')!='':
				res.rating=request.POST.get('rating')
			try:
				res.save()
				messages.add_message(request, messages.INFO, 'Profile Updated')
				return HttpResponseRedirect(reverse('dashboard'))
			except:
				pass
		return render(request,'profile.html',{'form':form,'type':type1})

	else:
		form=UserEditForm(request.POST)
		
		if form.is_valid():
			c=Customer(username=User(username=request.user.username))
			if request.POST.get('Location')!='':
				c.Location=request.POST.get('Location')

			try:
				c.save()
				return HttpResponseRedirect(reverse('dashboard'))
			except:
				pass

		return render(request,'profile.html',{'form':form,'type':type1})


def changePasswordView(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return HttpResponseRedirect(reverse('dashboard'))
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html', {'form': form})


def LogoutView(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))
