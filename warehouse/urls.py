from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workers/', views.worker_list, name='worker_list'),
    path('stock/', views.stock_list, name='stock_list'),
    path('issue/', views.issue_form, name='issue_form'),
    path('simulate/', views.run_simulation, name='run_simulation'),
    path('worn/', views.worn_items_list, name='worn_items'),
]