from django.urls import path, include
from ecomm.apps.company.views import (
	company
)


app_name = 'company'

urlpatterns = [
	path('home/', company.HomeView.as_view(), name='home'),
]