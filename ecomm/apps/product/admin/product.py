from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.product.models import (
	ProductBase,
	ProductBaseTranslation,
	Product,
	Media,
)

class ProductBaseTranslationInline(admin.StackedInline):
	model = ProductBaseTranslation
	extra = 1
	fieldsets = [
		('Translation', { 'fields': [
			('lang',), 
			('description',),
		]
		}),
		('SEO', {
			'fields': (
				('meta_keywords', 'meta_description',)
			)
		})
	]

@admin.register(ProductBase)
class ProductBaseAdmin(AdminBaseModel):
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'category',
				'company',
			)
		}),
	)
	list_display = [
		'slug', 
		'get_name',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'slug',
	]
	raw_id_fields = ['category',]
	inlines = [
		ProductBaseTranslationInline,
	]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default


class MediaInline(admin.StackedInline):
	model = Media
	extra = 1
	list_display = [
		'get_image',
		'get_alt',
		'is_showcase',
		'is_valid',
	]
	fieldsets = (
		(None, {
			'fields': (
				('is_valid', 'is_showcase',),
				'image',
				'alt',
			)
		}),
	)

	@admin.display(description='Alt')
	def get_alt(self, obj):
		return obj.alt_in_lang_or_default

	@admin.display(description='Image')
	def get_image(self, obj):
		return format_html(
			'<img width="120" height="120" src="{}" />'.format(
				obj.img_url_or_default('image', settings.DEFAULT_IMAGE['PLACEHOLDER'])
			)
		)

class ProductAttributeValuesInline(admin.StackedInline):
	model = Product.attribute_values.through
	extra = 1
	fieldsets = (
		(None, {
			'fields': (
				('attribute_values'),
			)
		}),
	)

@admin.register(Product)
class ProductAdmin(AdminBaseModel):
	def get_queryset(self, request):
		return super().get_queryset(request).select_related('prod_base')

	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'sku',
				'thumb',
				'ext_name',
				'prod_base',
				# 'brand',
				'product_type',
				'price',
				'sale_price',
				'is_default',
				'is_digital',
				'company'
			)
		}),
	)
	list_display = [
		'get_thumb',
		'slug', 
		'get_name',
		'price',
		'sale_price',
		'is_valid',
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'slug',
	]
	inlines = [
		ProductAttributeValuesInline,
		MediaInline,
	]
	search_fields = ('slug',)
	ordering = ('-created_at',)
	raw_id_fields = ['prod_base', 'product_type',]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Thumb')
	def get_thumb(self, obj):
		return format_html(
			'<img width="60" height="60" src="{}" />'.format(
				obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
			)
		)
