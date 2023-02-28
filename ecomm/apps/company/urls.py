from django.urls import path, include
from ecomm.apps.company.views import company
from ecomm.apps.company.views.shop import shop
from ecomm.apps.company.views.category import category
from ecomm.apps.company.views.product import product
from ecomm.apps.company.views.cart import cart
from ecomm.apps.cart.views import acts as cart_acts

app_name = 'company'

urlpatterns = [
	path('home/', company.HomeView.as_view(), name='home'),
	path('shop/', include([
		path('', shop.ShopView.as_view(), name='shop'),

		path('cart/', cart.CartView.as_view(), name='cart'),
		path('cart/add/', cart_acts.AddView.as_view(), name='add_cart'),
		path('cart/update/', cart_acts.UpdateView.as_view(), name='update_cart'),
		path('cart/delete/', cart_acts.DeleteView.as_view(), name='delete_cart'),

		path('<slug:cat_slug>/', category.CategoryView.as_view(), name='category'),
		path('<slug:cat_slug>/<slug:prod_slug>/', product.ProdictView.as_view(), name='product'),

	])),
]