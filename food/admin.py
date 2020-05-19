from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Order Database"
admin.site.site_tItle = "Order"
admin.site.index_title = "Order Database"

class OrderInline(admin.TabularInline):
    model = OrderedItems
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','restaurant_id','user_id','amount','status','order_date','delivery_boy_id','delivered_date']
    inlines = [OrderInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(Cart)

