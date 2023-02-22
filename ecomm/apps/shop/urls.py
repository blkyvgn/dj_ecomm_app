from django.urls import path, include
from ecomm.apps.shop.views import (
	shop
)


app_name = 'shop'

urlpatterns = [
	path('', shop.HomeView.as_view(), name='shop'),
]