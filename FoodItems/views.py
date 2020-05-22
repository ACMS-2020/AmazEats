from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from accounts.models import *
from .forms import FoodItemsForm,PriceForm,AcceptableForm,RestaurantForm
from .filters import ProductFilter
from .decorators import only_customer,only_restaurant
from django.contrib.auth.decorators import login_required


#VIEWS FOR CUSTOMER ACCOUNT

@login_required
@only_customer
def display_fooditems(request,username):
    print(request.POST)
    res = Restaurant.objects.get(pk = username)
    food = FoodItem.objects.filter(restaurant = res)
    pFilter = ProductFilter(request.POST , queryset = food)
    food = pFilter.qs
    return render(request,'food_customer/foodItems.html',{'food':food , 'pFilter' : pFilter, 'res':res })

@only_customer
def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    pFilter = ProductFilter(request.POST , queryset = restaurants)

    restaurants = pFilter.qs
    for r in restaurants:
        print(r.profile_pic)
    return render(request, 'food_customer/restaurants.html', {'restaurants': restaurants , 'pFilter':pFilter})

def search(request, username):
    query_string = ''
    res = Restaurant.objects.get(pk = username )
    if 'q' in request.GET:
        query_string = request.GET['q']
        food = FoodItem.objects.filter(restaurant = res ,food_name__icontains = query_string)
    else:
        food = FoodItem.objects.filter(restaurant = res)
    pFilter = ProductFilter(request.POST , queryset = food)
    food = pFilter.qs
    return render(request,'food_customer/foodItems.html',{'food':food , 'res':res , 'pFilter' : pFilter })

def fav_search(request, typ):
    query_string = ''
    user = Customer.objects.get(username=request.user.username)
    if 'q' in request.GET:
        if typ == 'fooditems':
            query_string = request.GET['q']
            res = set()
            food = FoodItem.objects.filter(food_name__icontains = query_string)
            for f in food:
                x= str(f.food_id)
                fav = Favourite.objects.filter(user_id = request.user.username , category_id=x)
                if(fav.exists()):
                    for y in fav:
                        id = int(y.category_id)
                        res.add(FoodItem.objects.get(pk=id))
        else:
            query_string = request.GET['q']
            res = user.favourite_set.filter(category_id__icontains = query_string,type='restaurants')
            
            for r in res:
                print(r.category_id)
    else:
        res = user.favourite_set.filter(type = typ)
    return render(request,'food_customer/favorites.html',{'res': res , 'type':typ })

def res_search(request):
    query_string = ''
    if 'q' in request.GET:
        query_string = request.GET['q']
        res = Restaurant.objects.filter(username__username__icontains = query_string)
        print(res)
    else:
        res = Restaurant.objects.all()
    pFilter = ProductFilter(request.POST , queryset = res)
    res = pFilter.qs
    return render(request,'food_customer/restaurants.html',{'restaurants': res , 'pFilter' : pFilter })

@only_customer
def res_favourites(request,username):
    user = Customer.objects.get(username=request.user.username)
    if (Favourite.objects.filter(category_id = username , user_id = user).exists()):
        pass
    else:
        fav = Favourite()
        fav.user_id = user
        fav.category_id = username
        fav.type = "restaurants"
        fav.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@only_customer
def food_favourites(request,id):
    user = Customer.objects.get(username=request.user.username)
    if (Favourite.objects.filter(category_id = str(id) , user_id = user).exists()):
        pass
    else:
        fav = Favourite()
        fav.user_id = user
        fav.category_id = str(id)
        fav.type = "fooditems"
        fav.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@only_customer
def favourites(request,type):
    print("favourites")
    user = Customer.objects.get(username=request.user.username)
    print(user)
    res = set()
    if(type == 'restaurants'):
        fav = user.favourite_set.filter(type = "restaurants")
        print(fav)
        for f in fav:
            r = Restaurant.objects.get(pk = f.category_id)
            res.add(r)
    else:
        fav = user.favourite_set.filter(type = "fooditems")
        for f in fav:
            category_id = int(f.category_id)
            r = FoodItem.objects.get(pk = category_id)
            res.add(r)
    return render(request, "food_customer/favorites.html" , { 'res' : res , 'type':type })

@only_customer
def input_reviews(request , id):
    food = FoodItem.objects.get(pk = id)
    if (Rating.objects.filter(food_id = food , user_id = request.user.username).exists()):
        r = Rating.objects.get(food_id = food , user_id = request.user.username)
        r.reviews = request.POST['reviews']
        r.save()
    else:
        reviews = request.POST['reviews']
        r = Rating(user_id = request.user.username,food_id = food, reviews = reviews)
        r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
@only_customer
def input_ratings(request , id):
    food = FoodItem.objects.get(pk = id)
    if (Rating.objects.filter(food_id = food , user_id = request.user.username).exists()):
        r = Rating.objects.get(food_id = food , user_id = request.user.username)
        r.rating = request.POST['rating']
        r.save()
    else:
        rating = request.POST['rating']
        r = Rating( user_id = request.user.username,food_id = food, rating = rating)
        r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@only_customer
def delete_favourites(request,id):
    id = str(id)
    user = Customer.objects.get(username=request.user.username)
    fav = Favourite.objects.get(category_id = id , user_id = user)
    fav.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#VIEWS FOR RESTAURANT ACCOUNT


@only_restaurant
def add_fooditems(request):
    form = FoodItemsForm()
    if request.method == "POST":
        form = FoodItemsForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit = False)
                res = Restaurant.objects.get(pk = request.user.username )
                instance.restaurant = res
                instance.save()
                return redirect('/fooditems/restaurant_fooditems')
            except:
                pass
    return render(request,'food_restaurant/index.html',{'form':form})

@only_restaurant
def display(request):
    res = Restaurant.objects.get(pk = request.user.username )
    food = FoodItem.objects.filter(restaurant = res)
    pFilter = ProductFilter(request.POST , queryset = food)
    food = pFilter.qs
    return render(request,'food_restaurant/show.html',{'food':food , 'pFilter' : pFilter})

@only_restaurant
def delete_fooditems(request,id):
    try:
        food = FoodItem.objects.get(pk=id)
    except FoodItem.DoesNotExist:
        raise Http404("Food item not found ")
    food.delete()
    return redirect("/fooditems/restaurant_fooditems")

@only_restaurant
def update_price(request,id):
    food = FoodItem.objects.get(pk=id)
    form = PriceForm(instance = food)
    print(food,form)
    if request.method == "POST":
        form =PriceForm(request.POST , instance = food)
        if form.is_valid():
            try:
                form.save()
                return redirect('/fooditems/restaurant_fooditems')
            except:
                pass
    return render(request,'food_restaurant/index.html',{'form':form})

@only_restaurant
def update_acceptable(request,id):
    food = FoodItem.objects.get(pk=id)
    if request.method == "POST":
        form = AcceptableForm(request.POST , instance = food)
        if form.is_valid():
            try:
                form.save()
                return redirect('/fooditems/restaurant_fooditems')
            except:
                pass
    else:
        form = AcceptableForm(instance = food)
    return render(request,'food_restaurant/index.html',{'form':form})

@only_restaurant
def create_restaurant(request):
    form= RestaurantForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/fooditems/restaurant_fooditems')
    return render(request, 'restaurant_templates/restaurants-form.html', {'form': form})

@only_restaurant
def update_restaurant(request, username):
    restaurant = Restaurant.objects.get(pk = username)
    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid():
        form.save()
        return redirect('/fooditems/restaurant_fooditems')
    return render(request, 'food_restaurant/restaurants-form.html', {'form': form, 'restaurant': restaurant})

@only_restaurant
def delete_restaurant(request, username):
    restaurant = Restaurant.objects.get(pk = username)

    if request.method == 'POST':
        restaurant.delete()
        return redirect('/fooditems/restaurant_fooditems')
    return render(request, 'food_restaurant/rest-delete-confirm.html', {'restaurant': restaurant})



