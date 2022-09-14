from django.urls import path
from . import views
  
urlpatterns = [
    path("uploadCharges", views.check_form_view,name = "uploadCharges"),
    path('showfrauds',views.showfrauds,name= "showfrauds"),
    path('uploadTrainData',views.GetTrainData,name = "uploadTrainData")
]