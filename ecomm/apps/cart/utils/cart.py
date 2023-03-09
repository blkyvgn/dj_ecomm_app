from decimal import Decimal
from django.utils.translation import get_language
from ecomm.apps.delivery.models import Delivery
from ecomm.apps.product.models import ( 
	Product, 
	ProductAttributeValue,
)
from django.db.models import (
	Prefetch, 
	F,
)


class Cart:
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		if 'cart' not in request.session:
			cart = self.session['cart'] = {}
		self.cart = cart

	def __iter__(self):
		product_ids = self.cart.keys()
		# products = Product.objs.valid().\
		# 	filter(id__in=product_ids).values(*Product.list_values)
		products = Product.objs.valid().filter(id__in=product_ids).\
			select_related('prod_base').select_related('prod_base__category').\
			prefetch_related('product_type__product_type_attributes').\
			prefetch_related(
				Prefetch(
					'attribute_values', 
					queryset=ProductAttributeValue.objs.valid().annotate(
						attr_slug=F('product_attribute__slug'),
					)
				)

			)

		cart = self.cart.copy()

		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def add(self, product, quantity):
		product_id = str(product.id)
		if product_id in self.cart:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}
		self.save()

	def get_product_ids(self):
		return [int(i) for i in self.cart.keys()]

	def update(self, product, quantity):
		product_id = str(product)
		if product_id in self.cart:
			self.cart[product_id]['quantity'] = quantity
		self.save()

	def get_total_price(self):
		newprice = 0.00
		subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

		if 'purchase' in self.session:
			newprice = Delivery.objs.valid().get(id=self.session['purchase']['delivery_id']).price

		total = subtotal + Decimal(newprice)
		return total

	def get_subtotal_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def get_product_quantity(self, product_id):
		item = self.cart.get(str(product_id), None)
		if item:
			return item['quantity']

	def get_product_total_price(self, product_id):
		item = self.cart.get(str(product_id), None)
		if item:
			return Decimal(item['price']) * item['quantity']

	def get_delivery_price(self):
		newprice = 0.00
		if 'purchase' in self.session:
			newprice = Delivery.objs.valid().get(id=self.session['purchase']['delivery_id']).price

		return newprice

	def add_delivery(self, delivery_id):
		if 'purchase' not in self.session:
			self.session['purchase'] = {
				'delivery_id': delivery_id,
			}
		else:
			self.session['purchase']['delivery_id'] = delivery_id
			self.save()

	def get_delivery_id(self):
		delivery_id = 0
		if 'purchase' in self.session:
			delivery_id = self.session['purchase']['delivery_id']
		return delivery_id
		
	def update_delivery(self, deliveryprice=0):
		subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
		total = subtotal + Decimal(deliveryprice)
		return total

	def delete(self, product):
		product_id = str(product)

		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def clear(self, key=None):
		# Remove cart from session
		if key is None:
			del self.session['cart']
			try:
				del self.session['address']
			except KeyError:
				pass
			try:
				del self.session['purchase']
			except KeyError:
				pass
		else:
			try:
				del self.session[key]
			except KeyError:
				pass
		self.save()
		
	def save(self):
		self.session.modified = True
