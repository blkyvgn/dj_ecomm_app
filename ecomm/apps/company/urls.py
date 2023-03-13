from django.urls import path, include
from ecomm.apps.company.views import company
from ecomm.apps.company.views.auth import (
	auth,
	passwd,
)
from ecomm.apps.company.views.shop import (
	shop, 
	search, 
	dashboard,
)
from ecomm.apps.company.views.category import category
from ecomm.apps.company.views.product import product
from ecomm.apps.company.views.cart import cart
from ecomm.apps.cart.views import acts as cart_acts
from ecomm.apps.company.views.compare import compare
from ecomm.apps.compare.views import acts as compare_acts
from ecomm.apps.company.views.wish import wish
from ecomm.apps.wish.views import acts as wish_acts
from ecomm.apps.company.views.order import order
from ecomm.apps.company.views.checkout import checkout 

app_name = 'company'

urlpatterns = [
	path('home/', company.HomeView.as_view(), name='home'),
	path('account/', include([
		path('registration/', auth.RegistrationView.as_view(), name='account_registration'),
		path('login/', auth.LoginView.as_view(), name='account_login'),
		path('logout/', auth.LogoutView.as_view(), name='account_logout'),
		path('activate/<slug:uidb64>/<slug:token>/', auth.ActivateView.as_view(), name='account_activate'),
		path('reset/passwd/', passwd.ResetPasswdView.as_view(), name='account_reset_passwd'),
		path('change/passwd/', passwd.ChangePasswdView.as_view(), name='account_change_passwd'),
		path('confirm/passwd/<slug:uidb64>/<slug:token>/', passwd.ConfirmPasswdView.as_view(), name='account_confirm_passwd'),

		path('dashboard/', dashboard.DashboardView.as_view(), name='account_dashboard'),
		path('checkout/', checkout.CheckoutView.as_view(), name='account_checkout'),

		path('order/list/', order.ListView.as_view(), name='account_order_list'),
	])),
	path('shop/', include([
		path('', shop.ShopView.as_view(), name='shop'),
		path('search/', search.SearchView.as_view(), name='search'),
		
		path('cart/', cart.CartView.as_view(), name='cart'),
		path('cart/add/', cart_acts.AddView.as_view(), name='add_cart'),
		path('cart/update/', cart_acts.UpdateView.as_view(), name='update_cart'),
		path('cart/delete/', cart_acts.DeleteView.as_view(), name='delete_cart'),

		path('compare/', compare.CompareView.as_view(), name='compare'),
		path('compare/add/', compare_acts.AddView.as_view(), name='add_compare'),
		path('compare/delete/', compare_acts.DeleteView.as_view(), name='delete_compare'),

		path('wish/', wish.WishView.as_view(), name='wish'),
		path('wish/add/', wish_acts.AddView.as_view(), name='add_wish'),
		path('wish/delete/', wish_acts.DeleteView.as_view(), name='delete_wish'),

		path('<slug:cat_slug>/', category.CategoryView.as_view(), name='category'),
		path('<slug:cat_slug>/<slug:prod_slug>/', product.ProdictView.as_view(), name='product'),
	])),
]