from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.cart.utils.cart import Cart

class CartDataMixin:

	def get_cart_data(self, **kwargs):
		context = kwargs
		context['cart'] = Cart(self.request)
		return context