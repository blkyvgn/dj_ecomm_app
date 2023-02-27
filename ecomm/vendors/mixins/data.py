from ecomm.apps.company.mixins.data import CompanyDataMixin
from ecomm.apps.category.mixins.data import CategoriesDataMixin
from django.http import Http404

class CommonDataMixin(CompanyDataMixin, CategoriesDataMixin):

	def dispatch(self, request, *args, **kwargs):
		company = self.get_company(**kwargs)
		setattr(request, 'company', company)
		return super().dispatch(request, *args, **kwargs)

	def get_common_data(self, **kwargs):
		context = kwargs
		context['company'] = self.request.company
		# context = self.get_company_data(**context)
		context = self.get_categories_data(**context)
		return context