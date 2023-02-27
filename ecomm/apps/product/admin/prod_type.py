from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.product.models import (
	ProductType,
)


class ProductTypeAttributeInline(admin.StackedInline):
	model = ProductType.product_type_attributes.through
	extra = 1
	fieldsets = [
		(None, 
			{ 'fields': ['prod_attribute']
		}),
	]
	search_fields = ('value',)


@admin.register(ProductType)
class ProductTypeAdmin(AdminBaseModel):
	list_display = [
		'get_thumb',
		'slug',
		'get_name', 
		'is_valid',
	]
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'thumb',
				'thumb_as',
				'category',
				'company',
			)
		}),
	)
	list_display_links = ('slug',)
	list_filter = (
		'is_valid', 
	)
	search_fields = ('slug',)
	ordering = ('-created_at',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ['category',]
	inlines = [
		ProductTypeAttributeInline,
	]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Thumb')
	def get_thumb(self, obj):
		if obj.thumb_as == ProductType.ThumbAs.HIDDEN:
			return format_html(settings.HIDDEN_SVG)
		if obj.thumb_as == ProductType.ThumbAs.IMG:
			return format_html(
				'<img width="60" height="60" src="{}" />'.format(
					obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
				)
			)
		if obj.thumb_as == ProductType.ThumbAs.SVG:
			return format_html(obj.svg)
