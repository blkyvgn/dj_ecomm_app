from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.cart.utils.cart import Cart

class NextUrlDataMixin:

	def get_next_url_data(self, **kwargs):
		context = kwargs
		if self.request.GET.get('next', False):
			context['next_url'] = self.request.GET['next']
		return context