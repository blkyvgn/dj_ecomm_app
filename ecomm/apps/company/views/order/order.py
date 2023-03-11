from django.conf import settings
from django.urls import reverse_lazy
from ecomm.vendors.base.view import ProtectBaseTemplateView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.vendors.helpers.request import get_filter_arguments
from ecomm.apps.order.models import Order
from django.db.models import F


class ListView(ProtectBaseTemplateView):
    permission_required = ['account.view_dashboard',]
    template_name = 'company/pages/order/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = []
        return context