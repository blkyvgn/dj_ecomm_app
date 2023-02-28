from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ecomm.vendors.mixins.data import CommonDataMixin

class BaseView(View):
	pass

class ProtectBaseView(LoginRequiredMixin, View):
	pass

class BaseTemplateView(CommonDataMixin, TemplateView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class ProtectBaseTemplateView(LoginRequiredMixin, CommonDataMixin, TemplateView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class BaseDetailView(CommonDataMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}

class ProtectBaseDetailView(LoginRequiredMixin, CommonDataMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**context)
		return {**context, **common_data}
