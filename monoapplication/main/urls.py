from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main, name='general_page'),
    path('main_page.html', include('transaction_management.urls')),
    path('index_product.html', include('productlinker.urls')),
    

    
]
