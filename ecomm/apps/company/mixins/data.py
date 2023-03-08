from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.apps.company.models import Company

class CompanyDataMixin:

	def get_company(self, **kwargs):
		company_alias = kwargs.get('alias')
		company = Company.get_from_cache_or_set(
			cache_key = company_alias, 
			timeout = settings.CACHE_TIMEOUT['YEAR']
		)
		if not company:
			raise Http404(_('Not found company with alias: %(alias)s' % {'alias': company_alias}))
		return company

	def get_company_data(self, **kwargs):
		context = kwargs
		context['company'] = self.get_company(**context)
		# company_alias = kwargs.get('alias')
		# company = Company.get_from_cache_or_set(
		# 	cache_key = company_alias, 
		# 	timeout = settings.CACHE_TIMEOUT['YEAR']
		# )
		# if not company:
		# 	raise Http404(_('Not found company with alias: %(alias)s' % {'alias': company_alias}))
		# setattr(self.request, 'company', {'id':company.id, 'alias':company.alias})
		# context['company'] = company
		return context


	
