from django.views import View
from django.views.generic.base import (
	TemplateResponseMixin,
	ContextMixin, 
	View,
	TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from ecomm.vendors.mixins.view import CommonDataMixin


class BaseView(CommonDataMixin, ContextMixin, View):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		common_data = self.get_common_data(**kwargs)
		return {**context, **common_data}

class ProtectBaseView(LoginRequiredMixin, BaseView):
	pass



class BaseTemplateView(TemplateResponseMixin, BaseView):
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)
	

class ProtectBaseTemplateView(TemplateResponseMixin, ProtectBaseView):
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

