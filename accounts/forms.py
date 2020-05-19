from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Customer,Restaurant,DeliveryAgent

user_type=[('restaurant','Restaurant'),('user','User'),('delivery','Delivery agent')]

class SignUpForm(UserCreationForm):

    fname = forms.CharField(max_length=30, required=False, help_text='Optional.')
    lname = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone= forms.CharField(max_length=11,required=True)
    usertype=forms.CharField(label="Select the type",widget=forms.Select(choices=user_type))
    class Meta:
        model = User
        fields = ('username', 'fname', 'lname', 'email', 'phone','password1', 'password2','usertype' )


class UserEditForm(forms.ModelForm):
	Location=forms.CharField(max_length=100,label='Location')
	class Meta:
		model = Customer
		fields=('Location',)

class RestaurantEditForm(forms.ModelForm):
	name=forms.CharField(max_length=20,required=False)
	Location=forms.CharField(max_length=100,required=False,label='Location')
	startTime=forms.TimeField(required=False)
	closeTime=forms.TimeField(required=False)
	cuisine=forms.CharField(max_length=20,required=False)
	pricePerHead=forms.IntegerField(required=False)
	contactNumber=forms.CharField(max_length=10,required=False)
	review=forms.CharField(max_length=20,required=False)
	class Meta:
		model = Restaurant
		fields=('name','Location','startTime','closeTime','cuisine','pricePerHead','contactNumber','review')

class DeliveryAgentEditForm(forms.ModelForm):
	rating=forms.CharField(max_length=20,required=False)
	vehicleNumber=forms.CharField(max_length=10,required=False)
	status=forms.BooleanField(required=False)
	drivingLicense=forms.CharField(max_length=13,required=False)

	class Meta:
		model = DeliveryAgent
		fields=('rating','vehicleNumber','status','drivingLicense')
