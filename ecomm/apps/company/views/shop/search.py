from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.vendors.helpers.request import get_filter_arguments
from ecomm.apps.product.models import (
    Product,
    ProductType,
    ProductTypeAttribute,
)
from django.db.models import F


class SearchView(BaseTemplateView):
    template_name = 'company/pages/shop/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_arguments = get_filter_arguments(self.request)
        products = Product.objs.valid().company(self.request.company.id).\
            annotate(
                units=F('stock_prod__units'),
                sold=F('stock_prod__units_sold'),
                cat_slug=F('prod_base__category__slug'),
            ).\
            select_related('prod_base').\
            filter_by_params(_or=True, 
                full_name__icontains=filter_arguments['full_name'],
                attribute_values__value__in=filter_arguments['attributes']
            ).\
            filter_by_params(
                price__gte=filter_arguments['price_min'],
                price__lte=filter_arguments['price_max']
            ).\
            filter(is_default=True).\
            order_by('-sold').distinct()
        context['products'] = paginator(self.request, products, per_page=settings.NUMBER_PER_PAGE)
        return context