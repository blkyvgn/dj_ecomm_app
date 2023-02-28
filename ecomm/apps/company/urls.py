from django.urls import path, include
from ecomm.apps.company.views import company
from ecomm.apps.company.views.shop import shop
from ecomm.apps.company.views.category import category
from ecomm.apps.company.views.product import product

app_name = 'company'

urlpatterns = [
	path('home/', company.HomeView.as_view(), name='home'),
	path('shop/', include([
		path('', shop.ShopView.as_view(), name='shop'),
		path('<slug:cat_slug>/', category.CategoryView.as_view(), name='category'),
		path('<slug:cat_slug>/<slug:prod_slug>/', product.ProdictView.as_view(), name='product'),
	])),
]