from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.company.models import (
	Company,
)


@admin.register(Company)
class CompanyAdmin(AdminBaseModel):
	model = Company
	list_display = (
		'get_logo',
		'alias',
		'get_name',
		'is_valid',
	)
	fieldsets = (
		(None, {
			'fields': (
				'alias',
				'name',
				'logo',
				'options',
				'is_valid',
			)
		}),
	)
	list_display_links = ('alias',)
	list_filter = (
		'is_valid', 
	)
	search_fields = ('alias',)
	ordering = ('-created_at',)
	prepopulated_fields = {'alias': ('name',)}

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