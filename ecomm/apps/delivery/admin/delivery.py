from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.delivery.models import (
	Delivery,
)

@admin.register(Delivery)
class DeliveryAdmin(AdminBaseModel):
	model = Delivery
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'name',
				'price',
				'method',
				'time_frame',
				'time_window',
				'position',
				'company',
			)
		}),
	)
	list_display = [
		'get_name',
		'price',
		'method',
		'time_frame',
		'time_window',
		'position',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'is_valid',
	]
	ordering = ('-created_at',)

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)