from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.mixins.model import (
	TimestampsMixin,
)
Account = get_user_model()

class Stock(BaseModel, TimestampsMixin):
	product = models.OneToOneField(
		'product.Product',
		related_name='stock_prod',
		on_delete=models.PROTECT,
	)
	last_checked = models.DateTimeField(
		null=True,
		blank=True,
	)
	units = models.IntegerField(
		default=0,
	)
	units_sold = models.IntegerField(
		default=0,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='stock_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='stock_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_stock',
	)

	class Meta:
		verbose_name = _('Stock')
		verbose_name_plural = _('Stocks')