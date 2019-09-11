from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:UniName>',views.UniReport,name ="UniReport"),
    path('result/<str:NAME>/<int:ID>',views.SpecificUni,name ="SpecificUni"),
    path('',views.HomePage, name="HomePage")


]
