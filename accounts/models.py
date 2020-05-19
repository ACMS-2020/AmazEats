from django.db import models
# Create your models here.
class User(models.Model):
	username=models.CharField(max_length=30,primary_key=True)
	fname=models.CharField(max_length=30)
	lname=models.CharField(max_length=30)
	phone=models.CharField(max_length=10)
	type1=models.CharField(max_length=10)
	email=models.EmailField(max_length=254)

	def __str__(self):
		return self.username


class Restaurant(models.Model):
	username=models.ForeignKey(User,editable=False,on_delete=models.CASCADE,primary_key=True)
	name=models.CharField(max_length=20,default="")
	Location=models.CharField(max_length=100,default="")
	startTime=models.TimeField(default="00:00")
	closeTime=models.TimeField(default="00:00")
	cuisine=models.CharField(max_length=20,default="")
	pricePerHead=models.IntegerField(default=0)
	contactNumber=models.CharField(max_length=10,default="")
	review=models.CharField(max_length=20,default="")
	image = models.ImageField()

class DeliveryAgent(models.Model):
	username=models.ForeignKey(User,editable=False,on_delete=models.CASCADE,primary_key=True)
	rating=models.CharField(max_length=20,default="")
	vehicleNumber=models.CharField(max_length=10,default="")
	status=models.BooleanField(default=False)
	drivingLicense=models.CharField(max_length=13,default="")


class Customer(models.Model):
	username=models.ForeignKey(User,editable=False,on_delete=models.CASCADE,primary_key=True)
	Location=models.CharField(max_length=100,default="")
