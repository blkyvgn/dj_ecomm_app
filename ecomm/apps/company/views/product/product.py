from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseDetailView
from ecomm.vendors.helpers.pagination import paginator
from django.utils.translation import get_language
from ecomm.vendors.helpers.orm import GroupConcat
from ecomm.apps.category.models import Category
from ecomm.apps.product.models import (
	Product,
	ProductType,
	ProductTypeAttribute,
	ProductBaseTranslation,
	ProductAttributeValue,
)
from django.http import Http404
from django.db.models import (
	Prefetch,
	F,
)


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
			select_related('product_type').\
			select_related('brand').\
			annotate(
				units=F('stock_prod__units'),
				cat_slug=F('prod_base__category__slug'),
				prods_slugs=GroupConcat('prod_base__base_prods__slug', True),
			).\
			filter(slug=prod_slug).first()
		if product is None:
			Http404('Not found product %(slug)s' % {'slug': prod_slug})
		return product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		product = kwargs.get('object')
		attributes = ProductTypeAttribute.objs.filter(prod_type=product.product_type).\
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

		prods_attribute_values = Product.objs.valid().company(self.request.company.id).\
			filter(slug__in=product.prods_slugs.split(',')).\
			values(
				attr_slug=F('attribute_values__product_attribute__slug'),
				val=F('attribute_values__value'),
				name=F('attribute_values__name')
			).distinct()

		context['attributes'] = attributes
		context['attribute_values'] = attribute_values
		context['prods_attribute_values'] = prods_attribute_values

		prod_translation = ProductBaseTranslation.objects.filter(
			prod_base=product.prod_base, 
			lang=get_language()
		).first()
		setattr(product, 'translate', prod_translation)

		return context



# class ProdictView(BaseDetailView):
# 	model = Product
# 	template_name = 'company/pages/product/detail.html'
# 	slug_url_kwarg = 'prod_slug'
# 	context_object_name = 'product'

# 	def get_object(self):
# 		prod_slug = self.kwargs.get(self.slug_url_kwarg, None)
# 		product = self.model.objs.valid().company(self.request.company.id).\
# 			select_related('brand').\
# 			select_related('prod_base').\
# 			select_related('prod_base__category').\
# 			select_related('product_type').\
# 			prefetch_related('media').\
# 			prefetch_related('product_type__product_type_attributes').\
# 			prefetch_related(
# 				Prefetch(
# 					'attribute_values', 
# 					queryset=ProductAttributeValue.objs.valid().annotate(
# 						attr_slug=F('product_attribute__slug'),
# 					)
# 				)
# 			).\
# 			annotate(
# 				units=F('stock_prod__units'),
# 			).\
# 			filter(slug=prod_slug).first()
# 		if product is None:
# 			Http404('Not found product %(slug)s' % {'slug': prod_slug})
# 		return product

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		product = kwargs.get('object')
# 		attributes = ProductTypeAttribute.objs.filter(prod_type=product.product_type).\
# 			values(
# 				slug=F('prod_attribute__slug'), 
# 				name=F('prod_attribute__name')
# 			).distinct()
# 		attribute_values = Product.objs.valid().company(self.request.company.id).\
# 			filter(slug=product.slug).\
# 			values(
# 				attr_slug=F('attribute_values__product_attribute__slug'),
# 				val=F('attribute_values__value'),
# 				name=F('attribute_values__name')
# 			).distinct()

# 		context['attributes'] = attributes
# 		context['attribute_values'] = attribute_values

# 		prod_translation = ProductBaseTranslation.objects.filter(
# 			prod_base=product.prod_base, 
# 			lang=get_language()
# 		).first()
# 		setattr(product, 'translate', prod_translation)

# 		return context