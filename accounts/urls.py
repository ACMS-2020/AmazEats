from django.urls import path
from .import views
from django.contrib.auth.views import LoginView ,LogoutView

urlpatterns= [path('',views.indexView,name="home"),
path('login/',views.loginView,name="login_url"),
path('register/',views.registerView,name="register_url"),
path('dashboard/',views.dashboardView,name="dashboard"),
path('logout/',views.LogoutView,name="logout"),
path('EditProfile/',views.EditProfileView,name="EditProfile"),
path('changePassword/',views.changePasswordView,name="changePassword"),
]
