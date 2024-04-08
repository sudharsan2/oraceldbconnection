from django.urls import path,include
from . import views

urlpatterns =[
    path('sqlquery',views.SQLQueryAPIView(),name= 'sqlquery'),
]