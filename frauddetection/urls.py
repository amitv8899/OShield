from django.urls import path
from . import views
  
urlpatterns = [
    path("uploadCharges", views.check_form_view),
]