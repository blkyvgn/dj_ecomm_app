from django.contrib import admin
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from ecomm.apps.account.models import (
	Address,
)


@admin.register(Address)
class AddressAdmin(AdminBaseModel):
	model = Address
	list_display = (
		'line',
		'town_city',
		'phone',
		'postcode',
		'default',
		'is_valid',
		'account',
	)
	list_filter = (
		'is_valid', 
	)
	fieldsets = (
		(None, {
			'fields': (
				'line',
				'town_city',
				'phone',
				'postcode',
				'delivery_instructions',
				'default',
				'is_valid',
				'account',
			)
		}),
	)
	search_fields = ('town_city', 'phone', 'account__email',)
	ordering = []
	raw_id_fields = ['account', ]