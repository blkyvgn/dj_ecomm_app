from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.sale.models import (
	Sale,
	Coupon,
	ProductSale,
)

@admin.register(ProductSale)
class ProductSaleAdmin(AdminBaseModel):
	model = ProductSale
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'product',
				'sale',
				'sale_price',
				'price_override',
				'company',
			)
		}),
	)
	list_display = [
		'product',
		'sale',
		'sale_price',
		'price_override',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'is_valid',
	]
	search_fields = ('product__slug', 'sale__slug',)
	ordering = ('-created_at',)
	raw_id_fields = ['product', 'sale',]

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)

@admin.register(Sale)
class SaleAdmin(AdminBaseModel):
	model = Sale
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'short_desc',
				'image',				
				'is_showcase',
				'sale_reduction',
				'is_schedule',
				'sale_start',
				'sale_end',
				'coupon',
				'company',
			)
		}),
	)
	list_display = [
		'get_image',
		'slug', 
		'get_name',
		'is_showcase',
		'sale_reduction',
		'is_schedule',
		'sale_start',
		'sale_end',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'is_valid',
		'is_showcase',
		'is_schedule',
	]
	search_fields = ('slug', 'sale_reduction',)
	list_display_links = ('slug',)
	ordering = ('-created_at',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ['coupon',]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Logo')
	def get_image(self, obj):
		return format_html(
			'<img width="200" height="50" src="{}" />'.format(
				obj.img_url_or_default('image', settings.DEFAULT_IMAGE['PLACEHOLDER'])
			)
		)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)