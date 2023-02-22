from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.shop.models import (
	Shop,
)


@admin.register(Shop)
class ShopAdmin(AdminBaseModel):
	model = Shop
	list_display = (
		'company',
		'is_valid',
	)
	list_filter = (
		'is_valid', 
	)
	fieldsets = (
		(None, {
			'fields': (
				'company',
				'is_valid',
				'options',
			)
		}),
	)
	ordering = ('-created_at',)