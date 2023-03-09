from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from ecomm.vendors.helpers.request import get_filter_arguments
from django.db.models import F
from ecomm.apps.product.models import Product


class HomeView(BaseTemplateView):
    template_name = 'company/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_arguments = get_filter_arguments(self.request)
        context['products'] = Product.objs.valid().company(self.request.company.id).\
            select_related('prod_base').\
            annotate(
                units=F('stock_prod__units'),
                sold=F('stock_prod__units_sold'),
                cat_slug=F('prod_base__category__slug'),
            ).\
            filter(is_default=True).\
            filter_by_params(_or=True, full_name__icontains=filter_arguments['full_name']).\
            distinct().\
            order_by('-sold')[:settings.NUMBER_PER_PAGE]
        return context
