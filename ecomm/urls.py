from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import (
    path, 
    include,
    re_path,
)
from django.conf.urls import (
    handler400,
    handler404, 
    handler500, 
    handler403, 
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('<slug:alias>/', include([
        path('', include('ecomm.apps.company.urls', namespace='company')),
        path('shop/', include('ecomm.apps.shop.urls', namespace='shop')),
    ])),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]

handler400 = 'ecomm.apps.company.views.error.error_400'
handler404 = 'ecomm.apps.company.views.error.error_404'
handler500 = 'ecomm.apps.company.views.error.error_500'
handler403 = 'ecomm.apps.company.views.error.error_403'
