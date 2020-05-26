import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = FoodItem
        fields = '__all__'
        exclude = ['food_id','food_name','restaurant','price','image','serviceable']
