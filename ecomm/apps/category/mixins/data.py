from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.category.models import Category

class CategoriesDataMixin:

	def get_categories_data(self, **kwargs):
		context = kwargs
		categories = Category.get_from_cache_or_set(
			cache_key = context['company'].alias, 
			query_set = Category.objs.valid().company(context['company'].id),
			timeout = settings.CACHE_TIMEOUT['YEAR']
		)
		context['categories'] = categories
		return context