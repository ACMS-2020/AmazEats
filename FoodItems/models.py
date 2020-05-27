from django.db import models

from accounts.models import *

# Items DataBase

class FoodItem(models.Model):
	food_id = models.AutoField(primary_key=True)
	food_name = models.CharField(max_length=100)
	restaurant = models.ForeignKey(Restaurant,on_delete = models.CASCADE)
	price = models.IntegerField()

	v_choice = [('Veg' , 'Veg'),('Non-veg' , 'Non-Veg')]
	item_choice = [('Starters', 'Starters'), ('Main Courses', 'Main Course'), ('Desserts', 'Desserts'), ('Beverages', 'Beverages')]
	s_choice = [('Service Available', 'Service Available'),('Service Not Available', 'Service Not Available')]

	item_type = models.CharField(choices=item_choice,max_length=50 ,blank=True,null=True )
	serviceable = models.CharField(max_length=30, choices=s_choice, default='Service Available')
	veg = models.CharField(max_length=100 , choices=v_choice, default='Veg')
	cuisine_type = models.CharField(max_length=100 ,blank=True,null=True)
	image = models.ImageField(upload_to='gallery/',blank=True,null=True,default="")

	def no_of_ratings(self):
		r = Rating.objects.filter(food_id = self).count()
		return r

	def avg_rating(self):
		sum=0
		ratings = Rating.objects.filter(food_id = self)
		for r in ratings:
			sum+=r.rating
		if (len(ratings)>0):
			return round(sum/len(ratings),1)
		return 0

#Rating Database for FoodItems

class Rating(models.Model):
	food_id = models.ForeignKey(FoodItem,on_delete = models.CASCADE)
	user_id = models.CharField(max_length=100 )
	rating = models.IntegerField(default = 0, null = True)
	reviews = models.TextField(max_length = 400 , null = True)

#Favourite DataBase

class Favourite(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(Customer,on_delete = models.CASCADE)
	category_id = models.CharField(max_length=30)
	type = models.CharField(max_length=30)


