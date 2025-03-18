from django.urls import path
from .views import *

urlpatterns=[
    path('stocks/',stock_list,name='show-stock'),
    path('stock_chart/<str:stock_name>/',stock_chart),
]




