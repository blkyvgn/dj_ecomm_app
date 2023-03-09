from django.urls import path, include
from ecomm.apps.account.views.auth import auth

app_name = 'account'

urlpatterns = [
	path('registration/', auth.RegistrationView.as_view(), name='registration'),
	path('login/', auth.LoginView.as_view(), name='login'),
]