from django.db import models
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
		unique=True
	)
	is_staff = models.BooleanField(
		default=False
	)
	is_active = models.BooleanField(
		default=True
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = AccountManager()

	class Meta:
		verbose_name =  _('Account')
		verbose_name_plural =  _('Accounts')
		ordering = ('-created_at',)
		permissions = [
			('view_dashboard', 'View page: Dashboard'),
			('change_password', 'Change account password'),
			('allow_chat', 'Allow chat'),
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
