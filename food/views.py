from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .decorators import *
from FoodItems.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#changes
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
#changes

from datetime import datetime
items_per_page = 8
# Create your views here.
'''
def display_items(request,res_id):
    items = FoodItem.objects.filter(restaurant_id=res_id)
    context = {'items':items}
    return render(request,'items.html',context)'''

@csrf_exempt
@only_customer
def addToCart(request,item_id):
    try:
        cartTrail = Cart.objects.get(user_id=request.user.username,food_id=str(item_id))
        cartTrail.quantity += 1
        cartTrail.save()
    except Cart.DoesNotExist:
        items = FoodItem.objects.filter(food_id=item_id)[0]
        #cart_obj = Cart.objects.filter(user_id=request.user.username)[0]
        cartItem = Cart.objects.create(user_id=request.user.username, res_id=items.restaurant.username.username, food_id=item_id,food_name=items.food_name,price=items.price)
        cartItem.save()
    print("added")
    return JsonResponse({'data':'Added'})
'''
@only_customer
def addToCart(request,item_id):
    try:
        cartTrail = Cart.objects.get(food_id=item_id)
        cartTrail.quantity += 1
        cartTrail.save()
    except Cart.DoesNotExist:
        items = FoodItem.objects.filter(food_id=item_id)[0]
        cartItem = Cart.objects.create(user_id=request.user.username, res_id=items.restaurant_id, food_id=item_id,food_name=items.food_name,price=items.price)
        cartItem.save()

    return HttpResponse("Added")

'''
@only_customer
def removeFromCart(request,item_id):
    cartTrail = Cart.objects.get(user_id=request.user.username,food_id=item_id)
    cartTrail.delete()
    return redirect('/food/cart')

@only_customer
def checkOut(request):
    cart = Cart.objects.filter(user_id=request.user.username)
    if(not cart.exists()):
        return render(request,"order_placed.html")
    order = Order.objects.create(user_id=request.user.username,restaurant_id=cart[0].res_id,order_date=datetime.now())
    for i in cart:
        order.order_set.create(item_id=i.food_id,quantity=i.quantity,item_name=i.food_name)
        item = FoodItem.objects.filter(food_id=i.food_id)
        order.amount += i.quantity*item[0].price
    order.save()
    cart.delete()
    return render(request,"order_placed.html")

@only_restaurant
def res_pending_order(request):
    obj = Order.objects.filter(restaurant_id=request.user.username,status="Placed")
    paginator = Paginator(obj,items_per_page)
    page = request.GET.get('page')
    if page==None:
        page = 1
    ind = int(page)-1
    obj = obj[ind*items_per_page:ind*items_per_page+items_per_page]
    values = paginator.get_page(page)
    context = {'obj':obj,'rest_id':request.user.username,'values':values}
    return render(request,'order_pending.html',context)

@only_restaurant
def res_processing_order(request):
    obj = Order.objects.filter(restaurant_id=request.user.username,status="Processing").order_by("-order_id")
    paginator = Paginator(obj,items_per_page)
    page = request.GET.get('page')
    if page==None:
        page = 1
    ind = int(page)-1
    obj = obj[ind*items_per_page:ind*items_per_page+items_per_page]
    values = paginator.get_page(page)
    context = {'obj':obj,'rest_id':request.user.username,'values':values}
    return render(request,'order_processed.html',context)

@only_restaurant
def res_dispatched_order(request):
    obj = Order.objects.filter(restaurant_id=request.user.username).exclude(status__in=['Processing','Placed','Rejected','Cancelled']).order_by("-order_date")
    paginator = Paginator(obj,items_per_page)
    page = request.GET.get('page')
    if page==None:
        page = 1
    ind = int(page)-1
    obj = obj[ind*items_per_page:ind*items_per_page+items_per_page]
    values = paginator.get_page(page)
    context = {'obj':obj,'rest_id':request.user.username,'values':values}
    return render(request,'order_dispatched.html',context)

@only_restaurant
def accept_order(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.order_accepted()
    obj.save()
    return redirect('/food/res_pending_order/')

@only_restaurant
def reject_order(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.order_rejected()
    return redirect('/food/res_pending_order/')

@only_restaurant
def processed_order(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.order_processed()
    obj.save()
    return redirect('/food/res_processing_order/')


@only_customer
def user_order_details(request):
    obj = Order.objects.filter(user_id=request.user.username).exclude(status="Delivered").exclude(status="Rejected").order_by('-order_id')
    print("user orders",len(obj))
    paginator = Paginator(obj, items_per_page)
    page = request.GET.get('page')
    if page == None:
        page = 1
    ind = int(page) - 1
    obj = obj[ind * items_per_page:ind * items_per_page + items_per_page]
    values = paginator.get_page(page)
    return render(request,'user_orders.html',{'obj':obj,'values':values})

@only_customer
def reorder(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    re_obj = Order.objects.create(user_id=obj.user_id,restaurant_id=obj.restaurant_id)
    items = obj.order_set.all()
    print(items)
    current_amount =0
    for i in items:
        print("In for",current_amount)
        re_obj.order_set.create(item_id=i.item_id,item_name=i.item_name,quantity=i.quantity)
        foo = FoodItem.objects.get(food_id=i.item_id)
        if foo:
            current_amount +=  foo.price*i.quantity
    re_obj.amount = current_amount
    re_obj.save()
    return JsonResponse({'data':'order placed'})

@only_delivery
def orders_available(request):
    obj = Order.objects.filter(status="In Delivery")
    paginator = Paginator(obj, items_per_page)
    page = request.GET.get('page')
    if page == None:
        page = 1
    ind = int(page) - 1
    obj = obj[ind * items_per_page:ind * items_per_page + items_per_page]
    values = paginator.get_page(page)
    return render(request, 'delivery_available.html', {'obj': obj, 'values': values,'delivery_boy_id':request.user.username})

@only_delivery
def your_delivery(request):
    obj = Order.objects.filter(delivery_boy_id=request.user.username).order_by('-order_date')
    paginator = Paginator(obj, items_per_page)
    page = request.GET.get('page')
    if page == None:
        page = 1
    ind = int(page) - 1
    obj = obj[ind * items_per_page:ind * items_per_page + items_per_page]
    values = paginator.get_page(page)
    return render(request, 'your_delivery.html', {'obj': obj, 'values': values})

@only_delivery
def accept_delivery(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.delivery_accepted()
    obj.delivery_boy_id=request.user.username
    obj.save()
    return redirect('/food/orders_available/')

@only_delivery
def order_picked(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.delivery_picked()
    obj.save()
    return redirect('/food/your_delivery/')

@only_delivery
def order_delivered(request,order_id):
    obj = Order.objects.get(order_id=order_id)
    obj.order_delivered()
    obj.save()
    return redirect('/food/your_delivery/')


@only_customer
def cart(request):
    obj =  Cart.objects.filter(user_id=request.user.username)
    food_images=dict()
    for i in obj:
        food = FoodItem.objects.get(food_id=i.food_id)
        if food_images.get(i.food_id)==None:
            food_images[i.food_id]=food.image.url
    print(food_images)
    return render(request,"cart.html",{'cart_items':obj,'food_images':food_images})


@only_customer
def cancel_order(request,order_id):
    obj = Order.objects.filter(order_id=order_id)
    obj.delete()
    return redirect('/food/user_orders/')

@only_customer
def order_history(request):
    not_needed = ['Delivered','Rejected']
    obj = Order.objects.filter(user_id=request.user.username,status__in=['Delivered','Rejected']).order_by('-order_id')
    print("obj length",len(obj))
    paginator = Paginator(obj,items_per_page)
    print("paginator",paginator)
    page = request.GET.get('page')
    if page == None:
        page = 1
    ind = int(page) - 1
    print(paginator.num_pages)
    obj = obj[ind * items_per_page:ind * items_per_page + items_per_page]
    values = paginator.get_page(page)
    return render(request, 'order_history.html', {'obj': obj, 'values': values, 'not_needed':not_needed})


@only_customer
@csrf_exempt
def alter_cart_items(request):
    if request.method == "POST":
        print("came here in alter")
        food_id = request.POST.get('food_id')
        food_item = Cart.objects.get(food_id=food_id)
        food_item.quantity = 0
        food_id.save()
    return JsonResponse({'data':'ok'})


