from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.compare.utils.compare import Compare

class CompareDataMixin:

	def get_compare_data(self, **kwargs):
		context = kwargs
		context['compare'] = Compare(self.request)
		return context