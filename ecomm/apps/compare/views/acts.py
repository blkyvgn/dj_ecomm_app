from django.conf import settings
from ecomm.vendors.base.view import BaseView
from ecomm.apps.compare.utils.compare import Compare
from ecomm.apps.product.models import Product
from django.http import JsonResponse
from django.shortcuts import ( 
	get_object_or_404, 
	redirect,
)
import json


class AddView(BaseView):
	def post(self, request, *args, **kwargs):
		comparison = Comparison(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		product = get_object_or_404(Product, id=item_id)
		comparison.add(product.id)
		comparison_filling = len(comparison)
		if request.user.is_authenticated:
			request.user.update_comparison(product.id, 'add')
		return JsonResponse({'quantity': comparison_filling})


class DeleteView(BaseView):
	def get(self, request, *args, **kwargs):
		comparison = Comparison(request)
		product = get_object_or_404(Product, slug=prod_slug)
		comparison.delete(product.id)
		if request.user.is_authenticated:
			request.user.update_comparison(product.id, 'remove')
		return redirect(request.META.get('HTTP_REFERER'))

	def post(self, request, *args, **kwargs):
		comparison = Comparison(request)
		result = json.loads(request.body)
		item_id = int(result['id'])
		product = get_object_or_404(Product, id=item_id)
		comparison.delete(product.id)
		comparison_filling = len(comparison)
		if request.user.is_authenticated:
			request.user.update_comparison(product.id, 'remove')
		return JsonResponse({'quantity': comparison_filling, 'id':item_id})