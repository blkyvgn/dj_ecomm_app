from ecomm.vendors.base.view import BaseTemplateView


class HomeView(BaseTemplateView):
    template_name = 'company/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context