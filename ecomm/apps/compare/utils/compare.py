from decimal import Decimal
from django.utils.translation import get_language
from ecomm.apps.product.models import Product
from django.db.models import F


class Compare:
	def __init__(self, request):
		self.session = request.session
		compare = self.session.get('compare')
		if 'compare' not in request.session:
			compare_prod_ids = request.user.get_compare(request.company.alias) if request.user.is_authenticated else []
			compare = self.session['compare'] = compare_prod_ids
		self.compare = compare

	def __iter__(self):
		product_ids = self.compare
		products = Product.objs.valid().\
			filter(id__in=product_ids).\
			select_related('prod_base').\
			prefetch_related('attribute_values__product_attribute').\
			annotate(
				units=F('stock_prod__units'),
				cat_slug=F('prod_base__category__slug'),
			)

		for prod in products:
			yield prod

	def __len__(self):
		return len(self.compare)

	def get_product_ids(self):
		return self.compare

	def add(self, product_id):
		product_id = str(product_id)
		if product_id not in self.compare:
			self.compare.append(str(product_id))
			self.save()

	def delete(self, product_id):
		product_id = str(product_id)
		if product_id in self.compare:
			self.compare.remove(product_id)
			self.save()

	def clear(self):
		del self.session['compare']
		self.save()
		
	def save(self):
		self.session.modified = True
