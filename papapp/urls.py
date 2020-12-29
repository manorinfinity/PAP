from collegeApp import views
from django.conf.urls import url
urlpatterns=[
    url('home',views.home),
    url('register',views.register),
    url('login',views.login),
    url('editProfile',views.editProfile),
    url('edit',views.edit),
]
