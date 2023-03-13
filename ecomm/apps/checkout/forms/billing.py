from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check
)

class BillingForm(forms.Form):
	first_name = forms.CharField(
		max_length=120,
	)
	last_name = forms.CharField(
		max_length=120,
	)
	email = forms.EmailField(
		max_length=120,
	)
	phone = forms.CharField(
		max_length=120,
	)
	address_line = forms.CharField(
		max_length=120,
	)
	address_line_2 = forms.CharField(
		max_length=120,
	)
	city = forms.CharField(
		max_length=120,
	)
	state = forms.CharField(
		max_length=120,
	)
	country = forms.ChoiceField(
		choices=settings.COUNTRIES,
	)
	order_note = forms.ChoiceField(
		widget=forms.Textarea()
	)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('E-mail')}
		)
		self.fields['first_name'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('First name')}
		)
		self.fields['last_name'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Last name')}
		)
		self.fields['phone'].widget.attrs.update(
			{'class': 'form-control', 'data-handlers':'keydown:onlyDigital', 'placeholder': _('Phone')}
		)
		self.fields['address_line'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Address')}
		)
		self.fields['address_line_2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Address')}
		)
		self.fields['city'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('City')}
		)
		self.fields['state'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('State')}
		)
		self.fields['country'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Country')}
		)
		self.fields['order_note'].widget.attrs.update(
			{'class': 'form-control', 'rows':'2', 'cols':'80', 'placeholder': _('Note')}
		)