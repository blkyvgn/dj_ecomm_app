from django.conf import settings
from ecomm.vendors.base.view import BaseView
from ecomm.apps.cart.utils.cart import Cart
from ecomm.apps.product.models import Product
from django.http import JsonResponse
from django.shortcuts import ( 
	get_object_or_404, 
	redirect,
)
import json

class AddView(BaseView):
	def post(self, request, *args, **kwargs):
		cart = Cart(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		item_quantity = int(result['quantity'])
		product = get_object_or_404(Product, id=item_id)
		cart.add(product=product, quantity=item_quantity)
		cart_filling = len(cart)
		return JsonResponse({'quantity': cart_filling})


class UpdateView(BaseView):
	def post(self, request, *args, **kwargs):
		cart = Cart(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		item_quantity = int(result['quantity'])
		cart.update(product=item_id, quantity=item_quantity)
		cart_filling = len(cart)
		cart_total = cart.get_total_price()
		cart_subtotal = cart.get_subtotal_price()
		prod_quantity = cart.get_product_quantity(item_id)
		prod_total_price = cart.get_product_total_price(item_id)
		return JsonResponse({
			'id': item_id,
			'quantity': cart_filling, 
			'total_price': cart_total,
			'subtotal_price': cart_subtotal,
			'prod_quantity': prod_quantity,
			'prod_total_price': prod_total_price,
		})


class DeleteView(BaseView):
	def post(self, request, *args, **kwargs):
		cart = Cart(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		cart.delete(product=item_id)
		cart_filling = len(cart)
		cart_total = cart.get_total_price()
		cart_subtotal = cart.get_subtotal_price()
		return JsonResponse({
			'id': item_id, 
			'quantity': cart_filling, 
			'total_price': cart_total,
			'subtotal_price': cart_subtotal,
		})