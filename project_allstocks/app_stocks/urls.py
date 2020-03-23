from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocks_list, name='stocks_list'),
]
