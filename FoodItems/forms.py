from django import forms
from .models import FoodItem
from accounts.models import Restaurant

class FoodItemsForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food_id','food_name','price','veg','item_type','cuisine_type','serviceable','image']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['Location', 'cuisine', 'contactNumber', 'pricePerHead',]
