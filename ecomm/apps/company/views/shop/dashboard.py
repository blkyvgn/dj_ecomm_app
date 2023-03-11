from django.conf import settings
from django.urls import reverse_lazy
from ecomm.vendors.base.view import ProtectBaseTemplateView


class DashboardView(ProtectBaseTemplateView):
    permission_required = ['account.view_dashboard',]
    template_name = 'company/pages/shop/dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context