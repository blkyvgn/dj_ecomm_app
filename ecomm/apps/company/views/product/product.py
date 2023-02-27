from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseDetailView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.apps.category.models import Category
from ecomm.apps.product.models import Product
from django.http import Http404
from django.db.models import F


class ProdictView(BaseDetailView):
	model = Product
	template_name = 'company/pages/product/detail.html'
	slug_url_kwarg = 'prod_slug'
	context_object_name = 'product'

	def get_object(self):
		prod_slug = self.kwargs.get(self.slug_url_kwarg, None)
		product = self.model.objs.valid().company(self.request.company.id).\
			filter(slug=prod_slug).first()
		if product is None:
			Http404('Not found product %(slug)s' % {'slug': prod_slug})
		return product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context