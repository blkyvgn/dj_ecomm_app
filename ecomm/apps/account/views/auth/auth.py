from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.mail import get_activate_account_mail_body
from ecomm.apps.company.tasks.mail import send_email_celery_task
from ecomm.vendors.base.view import BaseFormView
from ecomm.apps.account.forms.auth import (
	AccountRegistrationForm,
	AccountLoginForm,
)
from django.shortcuts import ( 
	get_object_or_404, 
	redirect,
	render,
)
from django.contrib.auth import (
	login, 
	logout, 
	authenticate,
)
import logging
logger = logging.getLogger('main')

class LoginView(BaseFormView):
	template_name = 'account/auth/login.html'
	form_class = AccountLoginForm
	redirect_authenticated_user = True

	def get_success_url(self, **kwargs): 
		return reverse_lazy('company:home', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		user = form.save(commit=False)
		email = loginForm.cleaned_data['email']
		password = loginForm.cleaned_data['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			user.is_active = True
			user.save()
			if self.request.POST['next_url']:
				return redirect(self.request.POST['next_url'])
			return redirect('account:dashboard')
		return super().form_valid(form)

	def invalid_form(self, form):
		messages.error(self.request, _('Error authenticate user'), extra_tags='alert-success')
		return super().invalid_form(form)


class RegistrationView(BaseFormView):
	template_name = 'account/auth/register.html'
	form_class = AccountRegistrationForm
	redirect_authenticated_user = True

	def get_success_url(self, **kwargs): 
		return reverse_lazy('company:home', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		user = form.save(commit=False)
		if user:
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['password'])
			user.is_active = False
			user.save()
			logger.info(f'REGISTRATION USER: {user.id}')
			# send registration email
			try:
				send_email_celery_task.delay(
					user.email, 
					get_activate_account_mail_body(self.request, user)
				)
				messages.success(self.request, 
					_('Accaunt created. For activation check mail'), extra_tags='alert-success'
				)
			except:
				messages.error(self.request, 
					_('E-Mail not sent'), extra_tags='alert-warning'
				)
		return super().form_valid(form)
