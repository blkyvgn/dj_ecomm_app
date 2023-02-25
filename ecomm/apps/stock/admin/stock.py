from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.stock.models import (
	Stock,
)

@admin.register(Stock)
class StockAdmin(AdminBaseModel):
	model = Stock
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'product',
				'last_checked',
				'units',
				'units_sold',
				'company',
			)
		}),
	)
	list_display = [
		'product',
		'last_checked',
		'units',
		'units_sold',
	]
	search_fields = ('product__slug',)
	ordering = ('-created_at',)
	raw_id_fields = ['product',]

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)