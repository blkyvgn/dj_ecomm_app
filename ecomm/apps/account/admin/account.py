from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from ecomm.apps.account.forms.admin.account import (
	AccountCreationForm, 
	AccountChangeForm,
)
from ecomm.apps.account.models import (
	Account,
)


@admin.register(Account)
class AccountAdmin(UserAdmin, AdminBaseModel):
	add_form = AccountCreationForm
	form = AccountChangeForm
	model = Account
	list_display = (
		'email', 
		'is_staff', 
		'is_active', 
		'_type',
	)
	list_filter = (
		'email', 
		'is_staff', 
		'is_active', 
		'_type',
	)
	fieldsets = (
		(None, {
			'fields': (
				'email', 
				'password',
			)
		}),
		('Permissions', {
			'fields': (
				'is_staff', 
				'is_active', 
				'_type', 
				'groups', 
				'user_permissions',
			)
		}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': (
				'email', 
				'password1', 
				'password2', 
				'is_staff', 
				'is_active', 
				'_type', 
				'groups', 
				'user_permissions',
			)}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)