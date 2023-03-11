from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.mixins.model import (
	TimestampsMixin,
)
Account = get_user_model()


class Comment(BaseModel, TimestampsMixin):
	username = models.CharField(
		max_length=50,
		null=True,
		blank=True,
	)
	product = models.ForeignKey(
		'Product',
		on_delete=models.PROTECT,
		related_name='comments',
	)
	account = models.ForeignKey(
		'account.Account',
		on_delete=models.PROTECT,
		related_name="media",
		null=True, 
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_prod_comments',
		null=True, 
		blank=True,
	)

	class Meta:
		verbose_name = _('Comment')
		verbose_name_plural = _('Comments')