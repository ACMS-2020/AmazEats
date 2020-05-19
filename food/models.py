from django.db import models
from datetime import datetime
from django.shortcuts import reverse

# Orders Databases

'''class FoodItem(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=100)
    restaurant_id = models.CharField(max_length=100)
    price = models.IntegerField()
    v_choice = [('veg' , 'veg'),('non-veg' , 'non-veg')]
    item_choice = [('Main Courses', 'Main Course'), ('Desserts', 'Desserts'), ('Beverages', 'Beverages')]
    item_type = models.CharField(choices=item_choice,max_length=50)
    s_choice = [('available', 'service available'),('not available', 'service not available')]
    serviceable = models.CharField(max_length=30, choices=s_choice, default='service available')
    image = models.ImageField(blank=True, null=True)
    veg = models.CharField(max_length = 30 , choices=v_choice , default='veg')
    cuisine_type = models.CharField(max_length=100)

    #def get_absolute_url(self):
    #    return reverse("hello",kwargs={})'''

class Cart(models.Model):
    user_id = models.CharField(max_length=100)
    res_id = models.CharField(max_length=100)
    food_id = models.CharField(max_length=100)
    food_name = models.CharField(max_length=100,default='No Name')
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def place_order(self):
        obj = Order(
            restaurant_id=self.res_id, user_id=self.user_id,order_date=datetime.now()
        )
        obj.save()

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    restaurant_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    amount = models.FloatField(default = 0)
    status_choices = [("Rejected","Rejected"),("Order Picked","Order Picked"),("Delivery Boy Assigned","Delivery Boy Assigned"),("Placed","Placed"),("Processing","Processing"),("In Delivery","In Delivery"),("Delivered","Delivered"),("Cancelled","Cancelled")]
    status = models.CharField(choices=status_choices,max_length=500,default="Placed")
    order_date = models.DateTimeField(default=datetime.now())
    delivery_boy_id = models.CharField(max_length=200,default="not_assigned")
    delivered_date = models.DateTimeField(blank=True, null=True)

    def order_accepted(self):
        if(self.status=="Placed"):
            self.status = "Processing"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def order_rejected(self):
        if(self.status=="Placed"):
            self.status = "Rejected"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def order_processed(self):
        if(self.status=="Processing"):
            self.status = "In Delivery"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def delivery_accepted(self):
        if(self.status=="In Delivery"):
            self.status = "Delivery Boy Assigned"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def delivery_picked(self):
        if(self.status=="Delivery Boy Assigned"):
            self.status = "Order Picked"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def order_delivered(self):
        if(self.status=="Order Picked"):
            self.status = "Delivered"
            self.delivered_date=datetime.now()
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

    def cancel_order(self):
        if(self.status=="Placed"):
            self.status="Cancelled"
            self.save()
            return True
        else:
            print("Invalid operation")
            return False

class OrderedItems(models.Model):
    items= models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_set")
    item_id = models.CharField(max_length=200)
    item_name = models.CharField(max_length=200,default="Food")
    quantity = models.IntegerField()

    def __str__(self):
        return self.item_id
