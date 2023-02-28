from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.mixins.model import (
	TimestampsMixin,
	HelpersMixin,
)
Account = get_user_model()


class Order(BaseModel, TimestampsMixin):
	account = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='order_account',
		null=True, 
		blank=True,
	)
	email = models.EmailField(
		max_length=254, 
		blank=True,
	)
	address = models.CharField(
		max_length=250,
	)
	city = models.CharField(
		max_length=100,
	)
	phone = models.CharField(
		max_length=100,
	)
	postal_code = models.CharField(
		max_length=20,
	)
	country_code = models.CharField(
		max_length=4, 
		blank=True,
	)
	total_paid = models.DecimalField(
		max_digits=5, 
		decimal_places=2,
	)
	order_key = models.CharField(
		max_length=200,
	)
	billing_status = models.BooleanField(
		default=False,
	)
	payment = models.CharField( # 'paypal'
		max_length=200, 
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_orders',
	)

	def __str__(self):
		return str(self.order_key)

	class Meta:
		verbose_name = _('Order')
		verbose_name_plural = _('Orders')
		ordering = ('-created_at',)

	

class OrderProduct(BaseModel):
	order = models.ForeignKey(
		Order, 
		related_name='order_orderproducts', 
		on_delete=models.CASCADE
	)
	product = models.ForeignKey(
		'product.Product', 
		related_name='prod_orderproducts', 
		on_delete=models.CASCADE
	)
	price = models.DecimalField(
		max_digits=5, 
		decimal_places=2
	)
	quantity = models.PositiveIntegerField(
		default=1
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_orders_products',
	)

	def __str__(self):
		return str(self.id)