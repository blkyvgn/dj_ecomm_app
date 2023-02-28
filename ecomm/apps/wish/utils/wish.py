from decimal import Decimal
from django.utils.translation import get_language
from ecomm.apps.product.models import Product



class Wish:
	def __init__(self, request):
		self.session = request.session
		wish = self.session.get('wish')
		if 'wish' not in request.session:
			wish_prod_ids = request.user.get_wish() if request.user.is_authenticated else []
			wish = self.session['wish'] = wish_prod_ids
		self.wish = wish

	def __iter__(self):
		product_ids = self.wish
		products = Product.objs.valid().\
			filter(id__in=product_ids).\
			select_related('prod_base')

		for prod in products:
			yield prod

	def __len__(self):
		return len(self.wish)

	def get_product_ids(self):
		return self.wish

	def add(self, product_id):
		self.wish.append(str(product_id))
		self.save()

	def delete(self, product_id):
		product_id = str(product_id)
		if product_id in self.wish:
			self.wish.remove(product_id)
			self.save()

	def clear(self):
		del self.session['wish']
		self.save()
		
	def save(self):
		self.session.modified = True
