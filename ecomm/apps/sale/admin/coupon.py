from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.sale.models import (
	Coupon,
)

@admin.register(Coupon)
class CouponAdmin(AdminBaseModel):
	model = Coupon
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'name',
				'coupon_code',
				'company',
			)
		}),
	)
	list_display = [
		'get_name',
		'coupon_code',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'is_valid',
	]
	search_fields = ('coupon_code',)
	ordering = ('-created_at',)

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)

