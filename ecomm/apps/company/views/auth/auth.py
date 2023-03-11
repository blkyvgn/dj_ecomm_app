from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.mail import get_activate_account_mail_body
from ecomm.apps.company.tasks.mail import send_email_celery_task
from ecomm.apps.account.models import Profile
from django.contrib.auth import get_user_model
from ecomm.vendors.base.view import ( 
	BaseFormView,
	ProtectBaseView,
)
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
Account = get_user_model()


class LoginView(BaseFormView):
	template_name = 'company/pages/account/auth/login.html'
	form_class = AccountLoginForm
	redirect_authenticated_user = True
	redirect_field_name = 'next'

	def get_success_url(self, **kwargs):
		if self.request.POST.get('next_url', False):
			return self.request.POST['next_url']
		return reverse_lazy('company:dashboard', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(self.request, email=email, password=password)
		if user is not None:
			login(self.request, user)
			user.is_active = True
			user.save(update_fields=['is_active'])
		else:
			messages.error(self.request, 
				_('Not found account'), extra_tags='alert-danger'
			)
		return super().form_valid(form)


class RegistrationView(BaseFormView):
	template_name = 'company/pages/account/auth/register.html'
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
			user.create_profile(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				phone = form.cleaned_data['phone'],
				sex = form.cleaned_data['sex'],
			)
			# Profile.objects.create(
			# 	first_name = form.cleaned_data['first_name'],
			# 	last_name = form.cleaned_data['last_name'],
			# 	phone = form.cleaned_data['phone'],
			# 	sex = form.cleaned_data['sex'],
			# 	account=user,
			# )
			logger.info(f'REGISTRATION USER: {user.id}')
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


class LogoutView(ProtectBaseView):
	permission_required = []

	def get(self, request, *args, **kwargs):
		user = get_object_or_404(Account, email=request.user.email)
		user.is_active = False
		user.save(update_fields=['is_active'])
		logout(request)
		logger.info(f'LOGOUT USER: {user.id}')
		return redirect('company:home', self.request.company.alias)
