from django.conf import settings
from ecomm.vendors.base.view import BaseTemplateView
from ecomm.vendors.helpers.pagination import paginator
from ecomm.apps.product.models import (
    Product,
    ProductType,
    ProductTypeAttribute,
)
from django.db.models import F


class ShopView(BaseTemplateView):
    template_name = 'company/pages/shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objs.valid().company(self.request.company.id).\
            annotate(
                units=F('stock_prod__units'),
                sold=F('stock_prod__units_sold'),
                cat_slug=F('prod_base__category__slug'),
            ).\
            select_related('prod_base').\
            order_by('-sold')
        context['products'] = paginator(self.request, products, per_page=settings.NUMBER_PER_PAGE)
        return context