from django.contrib.auth.backends import ModelBackend
from ecomm.apps.account.models import Account
import logging

logger = logging.getLogger('main')


class AccountBackend(ModelBackend):
	LOGIN_USER = 'LOGIN USER'
	LOGIN_USER_ERROR = 'LOGIN USER ERROR'
	
	def authenticate(self, request, email, password):    
		try:
			user = Account.objects.get(email=email)
			if user.check_password(password):
				logger.info(f'{self.LOGIN_USER}: {email}')
				return user
			else:
				return None
		except Account.DoesNotExist:
			logger.info(f'{self.LOGIN_USER_ERROR}: {email}')
			return None
		except Exception as e:
			logger.info(f'{self.LOGIN_USER_ERROR}: {email}')
			return None

	def get_user(self, user_id):
		try:
			user = Account.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None
		except Account.DoesNotExist:
			logger.info(f'{self.LOGIN_USER_ERROR}: {user_id}')
			return None