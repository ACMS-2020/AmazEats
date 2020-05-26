from django.db import models

from accounts.models import *
from django.core.validators import MaxValueValidator, MinValueValidator

# Items DataBases

class FoodItem(models.Model):
	food_id = models.AutoField(primary_key=True)
	food_name = models.CharField(max_length=100)
	restaurant = models.ForeignKey(Restaurant,on_delete = models.CASCADE)
	price = models.IntegerField()
	v_choice = [('veg' , 'veg'),('non-veg' , 'non-veg')]
	item_choice = [('Starters', 'Starters'), ('Main Courses', 'Main Course'), ('Desserts', 'Desserts'), ('Beverages', 'Beverages')]
	item_type = models.CharField(choices=item_choice,max_length=50 , null = True)
	s_choice = [('available', 'service available'),('not available', 'service not available')]
	serviceable = models.CharField(max_length=30, choices=s_choice, default='service available')
	veg = models.CharField(max_length=100 , choices=v_choice, default='veg')
	cuisine_type = models.CharField(max_length=100)
	image = models.ImageField(upload_to='gallery/',blank=True,null=True)

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


class Rating(models.Model):
	food_id = models.ForeignKey(FoodItem,on_delete = models.CASCADE)
	user_id = models.CharField(max_length=100 )
	rating = models.IntegerField(default = 0, null = True)
	reviews = models.TextField(max_length = 400 , null = True)

#Favourite DataBases

class Favourite(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(Customer,on_delete = models.CASCADE)
	category_id = models.CharField(max_length=30)
	type = models.CharField(max_length=30)

class Ustats(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=220)
    restaurant_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    food_item = models.CharField(max_length=220, default="item ordered")
    food_rating = models.PositiveIntegerField(default="1",
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    MCHOICES=[
	('January','January'),
	('February','February'),
	('March','March'),
	('April','April'),
	('May','May'),
	('June','June'),
	('July','July'),
	('August','August'),
	('September','September'),
	('October','October'),
	('November','November'),
	('December','December'),]
    month=models.CharField(default="month of ordering", choices=MCHOICES, max_length=10)
    order_placed = models.PositiveIntegerField(default="1",
        validators=[MinValueValidator(1), MaxValueValidator(1)])
    date_of_ordering = models.DateTimeField(blank=True, null=True)
    money_spent = models.PositiveIntegerField(default="1", validators=[MinValueValidator(1), MaxValueValidator(5000)])



    def __str__(self):
        return "{}-{}-{}".format(self.username, self.restaurant_name, self.restaurant_rating)


class Rstats(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    MCHOICES=[
	('January','January'),
	('February','February'),
	('March','March'),
	('April','April'),
	('May','May'),
	('June','June'),
	('July','July'),
	('August','August'),
	('September','September'),
	('October','October'),
	('November','November'),
	('December','December'),]
    month=models.CharField(default="month of ordering", choices=MCHOICES, max_length=10)
    order_placed = models.PositiveIntegerField(default="1", validators=[MinValueValidator(1), MaxValueValidator(5)])
    time=models.DateTimeField(blank=True, null=True)
    money_spent = models.PositiveIntegerField(default="1", validators=[MinValueValidator(1), MaxValueValidator(5000)])


    def __str__(self):
        return "{}-{}-{}".format(self.username, self.name, self.rating)




    	


