from django.contrib import admin
from ecomm.vendors.base.model import AdminBaseModel
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin
from ecomm.apps.fnd.models import (
	Order,
	OrderProduct,
)


@admin.register(Order)
class OrderAdmin(AdminBaseModel, ExcludeTimestampsMixin):
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'account',
				'address',
				'total_paid',
				'order_key',
				'billing_status', 
				'company',
			)
		}),
	)
	list_display = [
		'order_key', 
		'total_paid',
	]
	search_fields = (
		'account__email', 
		'address', 
		'order_key', 
		'total_paid', 
		'billing_status',
	)

@admin.register(OrderProduct)
class OrderProductAdmin(AdminBaseModel):
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'order',
				'product',
				'price',
				'quantity',
				'company',
			)
		}),
	)
	list_display = [
		'order', 
		'product',
		'price',
		'quantity',
		'is_valid', 
	]
	list_filter = [
		'is_valid',
	]
	search_fields = ('product_slug',)
	raw_id_fields = ['order', 'parent',]
	ordering = ('-created_at',)
	