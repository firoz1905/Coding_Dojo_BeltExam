"""TripBuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from loginregapp import views as lrv
from travelapp import views as trv

urlpatterns = [
    # path('admin/', admin.site.urls),
    ################# loginregapp Urls ###########
    path('',lrv.home),
    path('register',lrv.register),
    path('register/unique_email_check',lrv.unique_email_check),
    path('login',lrv.login),
    path('login/verify_ajax/',lrv.login_check_ajax),
    ################### Trabelapp Urls #############
    path('travels',trv.travels),
    path('travels/addtrip',trv.addtrip),
    path('travels/home',trv.home),
    path('travels/logout',trv.logout),
    path('travels/<int:trip_id>/join',trv.join,name="join"),
    path('travels/<int:trip_id>/cancel',trv.cancel,name="cancel"),
    path('travels/<int:trip_id>',trv.tripview,name="tripview"),
    path('travels/<int:trip_id>/delete',trv.delete,name="delete"),
]   


