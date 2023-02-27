from django.core.paginator import Paginator
from django.conf import settings

def paginator(request, objects, per_page=settings.NUMBER_PER_PAGE):
	paginator = Paginator(objects, per_page)
	page_number = request.GET.get('page')
	return paginator.get_page(page_number)