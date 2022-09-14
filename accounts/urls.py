from django.urls import path, include
from . import views


urlpatterns = [
    path("register",views.Register,name="register"),
    path('',include("django.contrib.auth.urls")),
    path('UserHome', views.UserHome),
]