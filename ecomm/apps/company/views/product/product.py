from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseDetailView
from ecomm.vendors.helpers.pagination import paginator
from django.utils.translation import get_language
from ecomm.apps.category.models import Category
from django.db.models import Prefetch
from ecomm.apps.product.models import (
	Product,
	ProductType,
	ProductTypeAttribute,
	ProductBaseTranslation,
)
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
			prefetch_related('media').\
			select_related('prod_base').\
			select_related('brand').\
			annotate(
				units=F('stock_prod__units'),
				cat_slug=F('prod_base__category__slug'),
			).\
			filter(slug=prod_slug).first()
		if product is None:
			Http404('Not found product %(slug)s' % {'slug': prod_slug})
		return product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		product = kwargs.get('object')
		attributes = ProductTypeAttribute.objs.filter(prod_type__prod__slug=product.slug).\
			values(
				slug=F('prod_attribute__slug'), 
				name=F('prod_attribute__name')
			).distinct()
		attribute_values = Product.objs.valid().company(self.request.company.id).\
			filter(slug=product.slug).\
			values(
				attr_slug=F('attribute_values__product_attribute__slug'),
				val=F('attribute_values__value'),
				name=F('attribute_values__name')
			).distinct()
		context['attributes'] = attributes
		context['attribute_values'] = attribute_values

		prod_translation = ProductBaseTranslation.objects.filter(
			prod_base=product.prod_base, 
			lang=get_language()
		).first()
		setattr(product, 'translate', prod_translation)

		return context