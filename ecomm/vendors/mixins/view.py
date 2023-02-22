from ecomm.apps.company.mixins.view import CompanyDataMixin


class CommonDataMixin(CompanyDataMixin):
	def get_common_data(self, **kwargs):
		context = kwargs
		company = self.get_company_data(**kwargs)
		context['company'] = company
		return context