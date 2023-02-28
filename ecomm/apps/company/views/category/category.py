from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseDetailView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.apps.category.models import Category
from django.db.models import Prefetch
from ecomm.apps.product.models import (
	Product,
	ProductType,
	ProductTypeAttribute,
)
from django.http import Http404
from django.db.models import F

class CategoryView(BaseDetailView):
	model = Category
	template_name = 'company/pages/category/item.html'
	slug_url_kwarg = 'cat_slug'
	context_object_name = 'category'

	def get_object(self):
		cat_slug = self.kwargs.get(self.slug_url_kwarg, None)
		category = self.model.objs.valid().company(self.request.company.id).\
			prefetch_related(
				Prefetch('prod_types', queryset=ProductType.objs.valid())
			).\
			filter(slug=cat_slug).first()
		if category is None:
			Http404('Not found category %(slug)s' % {'slug': cat_slug})
		return category

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = kwargs.get('object')

		attributes = ProductTypeAttribute.objs.valid().\
			filter(prod_type__prod__prod_base__category__slug=category.slug).\
			values(
				slug=F('prod_attribute__slug'), 
				name=F('prod_attribute__name'),
			).distinct()

		cat_tree = Category.objs.get(slug=category.slug).get_descendants(include_self=True)
		attribute_values = Product.objs.valid().company(self.request.company.id).\
			order_by().filter(is_default=True).\
			filter(prod_base__category__in=cat_tree).\
			values(
				attr_slug=F('attribute_values__product_attribute__slug'),
				val=F('attribute_values__value'),
				name=F('attribute_values__name'),
			).distinct()

		products = Product.objs.valid().company(self.request.company.id).\
			filter(prod_base__category__in=cat_tree).\
			annotate(
				units=F('stock_prod__units'),
				sold=F('stock_prod__units_sold'),
				cat_slug=F('prod_base__category__slug'),
			).\
			select_related('prod_base').\
			order_by('-sold')
		context['products'] = paginator(self.request, products, per_page=settings.NUMBER_PER_PAGE)
		context['attributes'] = attributes
		context['attribute_values'] = attribute_values
		return context