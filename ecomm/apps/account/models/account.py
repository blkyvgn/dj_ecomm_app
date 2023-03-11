from django.db import models
from django.conf import settings
from ecomm.vendors.base.model import BaseModel
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
	AbstractBaseUser, 
	PermissionsMixin,
)
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
)


class AccountManager(BaseUserManager):

	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The Email must be set'))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		extra_fields.setdefault('is_verified', True)
		extra_fields.setdefault('type', Account.Type.ADMIN)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, BaseModel, TimestampsMixin, SoftdeleteMixin):
	class Type(models.TextChoices):
		ADMIN    = 'ADMIN',    _('Admin')
		EMPLOYEE = 'EMPLOYEE', _('Employee')
		CUSTOMER = 'CUSTOMER', _('Customer')

	_type = models.CharField(db_column='type',
		max_length=15,
		choices=Type.choices,
		default=Type.CUSTOMER,
		verbose_name=(_('Type'))
	)

	email = models.EmailField(
		unique=True,
	)
	is_staff = models.BooleanField(
		default=False,
	)
	is_active = models.BooleanField(
		default=True,
	)
	is_verified = models.BooleanField(
		default=False,
	)
	wish = models.JSONField(
		null=True, 
		blank=True,
	)
	compare = models.JSONField(
		null=True, 
		blank=True,
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = AccountManager()

	class Meta:
		verbose_name =  _('Account')
		verbose_name_plural =  _('Accounts')
		ordering = ('-created_at',)
		permissions = [
			('view_dashboard',   'View page: Dashboard'),
			('change_password',  'Change account password'),
			('allow_chat',       'Allow chat'),
		]
		indexes = [
			models.Index(fields=['email',]),
		]

	def __str__(self):
		return self.email
		
	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, val):
		self._type = val

	@classmethod
	def get_by_uid(cls, uidb64):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64)) 
			user = cls.objs.get(pk=uid)
		except(TypeError, ValueError, OverflowError, user.DoesNotExist):
			user = None
		return user

	def get_wish(self, alias=settings.COMPANY_ALIAS):
		try:
			return self.wish[alias]
		except:
			return []

	def get_compare(self, alias=settings.COMPANY_ALIAS):
		try:
			return self.comparison[alias]
		except:
			return []

	def update_wish(self, prod_id, act='add', alias=settings.COMPANY_ALIAS):
		_wish = self.get_wish(alias)
		prod_id = str(prod_id)
		if act == 'add':
			_wish.append(prod_id)
		elif act == 'remove':
			if prod_id in _wish:
				_wish.remove(prod_id)
		else:
			raise ValueError('Update wish: illegal action')
		if self.wish:
			self.wish[alias] = list(set(_wish))
		else:
			self.wish = {alias: list(set(_wish))}
		self.save(update_fields=['wish'])

	def update_compare(self, prod_id, act='add', alias=settings.COMPANY_ALIAS):
		_compare = self.get_compare(alias)
		prod_id = str(prod_id)
		if act == 'add':
			_compare.append(prod_id)
		elif act == 'remove':
			if prod_id in _compare:
				_compare.remove(prod_id)
		else:
			raise ValueError('Update compare: illegal action')
		if self.compare:
			self.compare[alias] = list(set(_compare))
		else:
			self.compare = {alias: list(set(_compare))}
		self.save(update_fields=['compare'])

	


class AdminManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.ADMIN)

class Admin(Account):
	admin = AdminManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		self.is_staff = True
		self.type = Account.Types.ADMIN
		super().save(*args, **kwargs)


class EmployeeManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.EMPLOYEE)

class Employee(Account):
	employee = EmployeeManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		self.is_staff = True
		self.type = Account.Type.EMPLOYEE
		super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.CUSTOMER)

class Customer(Account):
	customer = CustomerManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		self.is_staff = False
		self.type = Account.Type.CUSTOMER
		super().save(*args, **kwargs)
