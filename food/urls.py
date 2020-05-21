from django.conf.urls import url
from django.urls import path
from . import views
from . views import *

app_name = "food"

urlpatterns=[

    #
    url(r'^addToCart/(?P<item_id>\d+)/$',views.addToCart,name="addToCart"),
    url(r'^removeFromCart/(?P<item_id>\d+)/$',views.removeFromCart,name="removeFromCart"),
    url('checkOut/',views.checkOut,name="checkOut"),
    url('res_pending_order/$',views.res_pending_order,name="res_pending_order"),
    url('res_processing_order/$',views.res_processing_order,name="res_processing_order"),
    url('res_dispatched_order/$',views.res_dispatched_order,name="res_dispatched_order"),
    url('accept_order/(?P<order_id>\d+)/$',views.accept_order,name="accept_order"),
    url('processed_order/(?P<order_id>\d+)/$',views.processed_order,name="processed_order"),
    url('user_orders/',views.user_order_details,name="user_orders"),
    url('reorder/(?P<order_id>\d+)/$',views.reorder,name="reorder"),
    url('accept_delivery/(?P<order_id>\d+)/$',views.accept_delivery,name="accept_delivery"),
    url('orders_available/',views.orders_available,name="orders_available"),
    url('your_delivery/',views.your_delivery,name="your_delivery"),
    url('order_picked/(?P<order_id>\d+)/$',views.order_picked,name="order_picked"),
    url('order_delivered/(?P<order_id>\d+)/$',views.order_delivered,name="order_delivered"),
    url('reject/(?P<order_id>\d+)/$',views.reject_order,name="reject"),
    url('cart/',views.cart,name="cart"),
    url('cancelorder/(?P<order_id>\d+)/$',views.cancel_order,name="cancel"),
    url('cartalter/(?P<food_id>\d+)/(?P<quantity>\d+)/$',views.cartalter,name="cartalter"),
    url('order_history/',views.order_history,name="order_history"),
    url('alter_cart/(?P<food_id>\d+)/(?P<quantity>\d+)/$',views.alter_cart_items,name="alter_cart"),
]
