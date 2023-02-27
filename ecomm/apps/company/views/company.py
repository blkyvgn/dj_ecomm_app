from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from ecomm.apps.product.models import Product


class HomeView(BaseTemplateView):
    template_name = 'company/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.get_popular(self.request.company.id, settings.NUMBER_PER_PAGE)
        return context
