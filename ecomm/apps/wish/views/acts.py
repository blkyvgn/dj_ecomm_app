from django.conf import settings
from ecomm.vendors.base.view import BaseView
from ecomm.apps.wish.utils.wish import Wish
from ecomm.apps.product.models import Product
from django.http import JsonResponse
from django.shortcuts import ( 
	get_object_or_404, 
	redirect,
)
import json


class AddView(BaseView):
	def post(self, request, *args, **kwargs):
		wish = Wish(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		product = get_object_or_404(Product, id=item_id)
		wish.add(product.id)
		wish_filling = len(wish)
		if request.user.is_authenticated:
			request.user.update_wish(product.id, act='add', alias=request.company.alias)
		return JsonResponse({'quantity': wish_filling})


class DeleteView(BaseView):
	def get(self, request, *args, **kwargs):
		wish = Wish(request)
		product = get_object_or_404(Product, slug=prod_slug)
		wish.delete(product.id)
		if request.user.is_authenticated:
			request.user.update_wish(product.id, act='remove', alias=request.company.alias)
		return redirect(request.META.get('HTTP_REFERER'))

	def post(self, request, *args, **kwargs):
		wish = Wish(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		product = get_object_or_404(Product, id=item_id)
		wish.delete(product.id)
		wish_filling = len(wish)
		if request.user.is_authenticated:
			request.user.update_wish(product.id, act='remove', alias=request.company.alias)
		return JsonResponse({'quantity': wish_filling, 'id':item_id})