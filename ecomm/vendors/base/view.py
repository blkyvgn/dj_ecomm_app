from django.views import View
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from ecomm.vendors.mixins.data import CommonDataMixin
from django.views.generic.edit import FormView


class BaseView(CommonDataMixin, View):
	pass

class ProtectBaseView(CommonDataMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
	
	def get_login_url(self):
		return reverse_lazy('company:login', args = (self.request.company.alias,))

class BaseTemplateView(CommonDataMixin, TemplateView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class ProtectBaseTemplateView(CommonDataMixin, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

	def get_login_url(self):
		return reverse_lazy('company:login', args = (self.request.company.alias,))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class BaseDetailView(CommonDataMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class ProtectBaseDetailView(CommonDataMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):

	def get_login_url(self):
		return reverse_lazy('company:login', args = (self.request.company.alias,))
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class BaseFormView(CommonDataMixin, FormView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}