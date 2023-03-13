from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from ecomm.vendors.helpers.token import account_token
from ecomm.vendors.helpers.mail import get_reset_passwd_mail_body
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ecomm.vendors.base.view import ( 
	BaseFormView,
	BaseView,
)
from ecomm.apps.account.forms.passwd import (
	PwdMailForm,
	PwdChangeForm,
)
from django.shortcuts import ( 
	get_object_or_404, 
	redirect,
	render,
)
import logging
logger = logging.getLogger('main')
Account = get_user_model()


class ResetPasswdView(BaseFormView):
	template_name = 'company/pages/account/auth/reset.html'
	form_class = PwdMailForm
	redirect_authenticated_user = True

	def get_success_url(self, **kwargs):
		return reverse_lazy('company:home', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		email = form.cleaned_data['email']
		user = Account.objs.get(email=email)
		try:
			send_email_celery_task.delay(user.email, get_reset_passwd_mail_body(request, user))
			messages.success(self.request, _('E-Mail send. Check mail'), extra_tags='alert-success')
		except:
			print('----------------------- mail body -------------------------')
			print(get_reset_passwd_mail_body(self.request, user))
			print('----------------------- ********* -------------------------')
			messages.error(self.request, _('E-Mail not sent'), extra_tags='alert-danger')
		return super().form_valid(form)


class ChangePasswdView(BaseFormView):
	template_name = 'company/pages/account/auth/confirm.html'
	# form_class = PwdChangeForm
	redirect_authenticated_user = True

	def get_form(self):
		user = Account.get_by_uid(self.request.session['user_uid'])
		return PwdChangeForm(user, self.request.POST)

	def get_success_url(self, **kwargs):
		return reverse_lazy('company:home', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		user = Account.get_by_uid(self.request.session['user_uid'])
		if user is not None:
			form.save()
			messages.success(self.request, _('Password changed'), extra_tags='alert-success')
			del self.request.session['user_uid']
		else:
			messages.error(self.request, _('Password not changed'), extra_tags='alert-danger')
		return super().form_valid(form)


class ConfirmPasswdView(BaseView):
	def get(self, request, *args, **kwargs):
		user = Account.get_by_uid(kwargs['uidb64'])
		if user is not None and account_token.check_token(user, kwargs['token']):
			self.request.session['user_uid'] = kwargs['uidb64']
			return redirect('company:account_change_passwd', self.request.company.alias)
		else:
			messages.success(self.request, _('Invalid get user by token'), extra_tags='alert-danger')
			return redirect('company:home', self.request.company.alias)
		