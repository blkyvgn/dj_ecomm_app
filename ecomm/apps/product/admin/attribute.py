from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.product.models import (
	ProductAttribute,
	ProductAttributeValue,
)

class ProductAttributeValueAdmin(admin.StackedInline):
	model = ProductAttributeValue
	extra = 1
	list_display = [
		'value',
		'get_name',
		'is_valid',
	]
	fieldsets = [
		(None, { 
			'fields': [
				('is_valid',), 
				'value',
				'name', 
			]
		})
	]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default


@admin.register(ProductAttribute)
class ProductAttributeAdmin(AdminBaseModel):
	list_display = (
		'get_thumb',
		'slug', 
		'get_name',
		'is_valid', 
	)
	list_display_links = ('slug',)
	list_filter = (
		'is_valid', 
	)
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'thumb',
				'svg',
				'thumb_as',
				'company', 
			)
		}),
	)
	search_fields = ('slug',)
	ordering = ('-created_at',)
	prepopulated_fields = {'slug': ('name',)}

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Thumb')
	def get_thumb(self, obj):
		if obj.thumb_as == ProductAttribute.ThumbAs.HIDDEN:
			return format_html(settings.HIDDEN_SVG)
		if obj.thumb_as == Category.ThumbAs.IMG:
			return format_html(
				'<img width="60" height="60" src="{}" />'.format(
					obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
				)
			)
		if obj.thumb_as == ProductAttribute.ThumbAs.SVG:
			return format_html(obj.svg)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)

	inlines = [
		ProductAttributeValueAdmin,
	]