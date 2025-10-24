from django.urls import path, include

from . import views

urlpatterns = [
    path('transactions/table_transaction/', views.table_transaction, name='table_transaction'),
    path('transactions/add_transaction/', views.add_transaction, name='add_transaction'),
]
