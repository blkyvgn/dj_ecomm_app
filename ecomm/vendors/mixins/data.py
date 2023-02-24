from ecomm.apps.company.mixins.data import CompanyDataMixin
from ecomm.apps.category.mixins.data import CategoriesDataMixin


class CommonDataMixin(CompanyDataMixin, CategoriesDataMixin):
	def get_common_data(self, **kwargs):
		context = kwargs
		context = self.get_company_data(**context)
		context = self.get_categories_data(**context)
		return context