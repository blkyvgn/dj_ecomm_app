from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseDetailView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.apps.category.models import Category
from ecomm.apps.product.models import Product
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
			filter(slug=cat_slug).first()
		if category is None:
			Http404('Not found category %(slug)s' % {'slug': cat_slug})
		return category

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = kwargs.get('object')
		products = Product.objs.valid().company(self.request.company.id).\
			filter(
				prod_base__category__in=Category.objs.get(slug=category.slug).get_descendants(include_self=True)
			).\
			annotate(
				units=F('stock_prod__units'),
				sold=F('stock_prod__units_sold')
			).\
			select_related('prod_base').\
			order_by('-sold')
		context['products'] = paginator(self.request, products, per_page=settings.NUMBER_PER_PAGE)
		return context