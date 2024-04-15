from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug>/', product_detail_view, name='product_detail'),
    path('search/<slug>/', category_list, name='category_list'),
]
