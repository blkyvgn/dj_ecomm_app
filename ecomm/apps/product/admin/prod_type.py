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
		'slug',
		'get_name', 
	]
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
