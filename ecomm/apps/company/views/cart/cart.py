from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from ecomm.vendors.helpers.pagination import paginator
from django.db.models import F


class CartView(BaseTemplateView):
	template_name = 'company/pages/cart/cart.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context