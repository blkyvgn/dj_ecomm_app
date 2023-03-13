from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView, BaseFormView, ProtectBaseFormView
from ecomm.apps.checkout.forms.billing import BillingForm
from django.contrib.auth import get_user_model
Account = get_user_model()


class CheckoutView(ProtectBaseFormView):
	permission_required = ['account.view_dashboard',]
	template_name = 'company/pages/checkout/checkout.html'
	form_class = BillingForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.request.user.is_authenticated:
			kwargs['initial'] = self.request.user.get_checkout_form_initialize_data()
		return kwargs

	def get_success_url(self, **kwargs):
		return reverse_lazy('company:account_dashboard', args = (self.request.company.alias,))
	
	def form_valid(self, form):
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
