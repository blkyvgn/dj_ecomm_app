from django.urls import path, include
from ecomm.apps.company.views import company
from ecomm.apps.company.views.shop import shop
from ecomm.apps.company.views.category import category

app_name = 'company'

urlpatterns = [
	path('home/', company.HomeView.as_view(), name='home'),
	path('shop/', shop.ShopView.as_view(), name='shop'),
	path('category/<slug:cat_slug>/', category.CategoryView.as_view(), name='category'),
]