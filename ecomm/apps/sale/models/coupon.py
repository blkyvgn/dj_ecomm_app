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

class Coupon(BaseModel, TimestampsMixin, HelpersMixin):
	name = models.JSONField(
		max_length=500,
	)
	coupon_code = models.CharField(
		max_length=20,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='coupon_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='coupon_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_coupons',
	)

	def __str__(self):
		return self.coupon_code

	class Meta:
		verbose_name = _('Coupon')
		verbose_name_plural = _('Coupons')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'coupon_code'], name='unique_coupon_code_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'coupon_code')), # condition='TRUE'
		]