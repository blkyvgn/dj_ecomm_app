from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.wish.utils.wish import Wish

class WishDataMixin:

	def get_wish_data(self, **kwargs):
		context = kwargs
		context['wish'] = Wish(self.request)
		return context