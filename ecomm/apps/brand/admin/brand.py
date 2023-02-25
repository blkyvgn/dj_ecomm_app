from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.brand.models import (
	Brand,
)

@admin.register(Brand)
class BrandAdmin(AdminBaseModel):
	model = Brand
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'site_url',
				'logo',
				'company',
			)
		}),
	)
	list_display = [
		'get_logo',
		'slug', 
		'get_name',
		'is_valid', 
	]
	list_editable = [
		'is_valid',
	]
	list_filter = [
		'is_valid',
	]
	list_display_links = ('slug',)
	search_fields = ('slug',)
	ordering = ('-created_at',)
	prepopulated_fields = {'slug': ('name',)}

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Logo')
	def get_logo(self, obj):
		return format_html(
			'<img width="80" src="{}" />'.format(
				obj.img_url_or_default('logo', settings.DEFAULT_IMAGE['LOGO'])
			)
		)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)