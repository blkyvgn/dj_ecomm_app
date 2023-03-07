from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from django.db.models import F
from ecomm.apps.product.models import Product


class WishView(BaseTemplateView):
    template_name = 'company/pages/wish/wish.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context