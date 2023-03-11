from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check
)
from ecomm.apps.account.models import Profile
from ecomm.apps.account.models.account import Customer


class AccountLoginForm(forms.Form):
	email = forms.EmailField(
		max_length=120
	)
	password = forms.CharField(
		widget=forms.PasswordInput()
	)
	# next_url = forms.CharField(
	# 	widget=forms.HiddenInput(), 
	# 	required=False
	# )
	def clean_password(self):
		passwd = self.cleaned_data['password']
		passwd_validation_check(passwd, _('Not valid password'))
		return passwd

	def clean_email(self):
		email = self.cleaned_data['email']
		email_validation_check(email, _('Not valid email'))
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('E-mail')}
		)
		self.fields['password'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Password')}
		)

class AccountRegistrationForm(forms.ModelForm):
	first_name = forms.CharField(
		label=_('First name'), 
		min_length=4, 
		max_length=20, 
	)
	last_name = forms.CharField(
		label=_('First name'), 
		min_length=4, 
		max_length=20, 
	)
	phone = forms.CharField(
		label=_('Phone'), 
		min_length=4, 
		max_length=20, 
	)
	sex = forms.ChoiceField(
		widget=forms.RadioSelect, 
		choices=Profile.Sex.choices,
		initial=Profile.Sex.MALE,
	)
	# country = forms.ChoiceField(
	# 	choices=settings.COUNTRIES,
	# )
	# sex = forms.ChoiceField(
	# 	widget=forms.RadioSelect, 
	# 	choices=SEX,
	# 	initial='male',
	# )
	# city = forms.CharField(
	# 	label=_('City'), 
	# 	min_length=4, 
	# 	max_length=20, 
	# )
	# username = forms.CharField(
	# 	label='Username', 
	# 	min_length=4, 
	# 	max_length=20, 
	# 	help_text='Required'
	# )
	email = forms.EmailField(
		max_length=100, 
		help_text='Required', 
		error_messages={
			'required': _('Sorry, you will need an email')
		}
	)
	password = forms.CharField(
		label=_('Password'), 
		widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label=_('Repeat password'), 
		widget=forms.PasswordInput
	)

	class Meta:
		model = Customer
		# fields = ('username', 'email',)
		fields = ('email',)

	# def clean_username(self):
	# 	username = self.cleaned_data['username'].lower()
	# 	r = Account.objs.filter(username=username)
	# 	if r.count():
	# 		raise forms.ValidationError(_('Username already exists'))
	# 	return username

	def clean_password(self):
		passwd = self.cleaned_data['password']
		passwd_validation_check(passwd, _('Not valid password'))
		return passwd

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError(_('Passwords do not match.'))
		return cd['password']

	def clean_email(self):
		email = self.cleaned_data['email']
		if Customer.objs.filter(email=email).exists():
			raise forms.ValidationError(
				_('Please use another Email, that is already taken'))
		return email

	def __init__(self, *args, **kwargs): 
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('First name')})
		self.fields['last_name'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Last name')})
		self.fields['phone'].widget.attrs.update(
			{'class': 'form-control', 'data-handlers':'keydown:onlyDigital', 'placeholder': _('Phone')})
		self.fields['sex'].widget.attrs.update(
			{'class': 'custom-control-input'})
		# self.fields['country'].widget.attrs.update(
		# 	{'class': 'form-control', 'id':'inputState'})
		# self.fields['city'].widget.attrs.update(
		# 	{'class': 'form-control', 'placeholder': _('City')})
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control', 'type':'email', 'placeholder': _('E-mail')})
		self.fields['password'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Password')})
		self.fields['password2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': _('Repeat Password')})
