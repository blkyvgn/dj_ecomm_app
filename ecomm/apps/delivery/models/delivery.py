from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
	MinValueValidator,
	MaxValueValidator,
)
from decimal import Decimal
from ecomm.vendors.mixins.model import (
	TimestampsMixin,
	HelpersMixin,
)
Account = get_user_model()

class Delivery(BaseModel, TimestampsMixin, HelpersMixin):
	class Types(models.TextChoices):
		IS = 'IS', _('In Store')
		HD = 'HD', _('Home Delivery')
		DD = 'DD', _('Digital Delivery')

	name = models.JSONField(
		help_text=_('Required'),
	)
	price = models.DecimalField(
		verbose_name=_('delivery price'),
		help_text=_('Maximum 999.99'),
		error_messages={
			'name': {
				'max_length': _('The price must be between 0 and 999.99.'),
			},
		},
		max_digits=5,
		decimal_places=2,
		validators=[
			MinValueValidator(settings.MIN_PRICE),
			MaxValueValidator(settings.MAX_PRICE),
		],
	)
	method = models.CharField(
		choices=Types.choices,
		default=Types.IS,
		verbose_name=_('delivery_method'),
		help_text=_('Required'),
		max_length=255,
	)
	time_frame = models.CharField( # 2-3 days
		verbose_name=_('delivery timeframe'),
		help_text=_('Required'),
		max_length=255,
		null = True,
		blank = True,
	)
	time_window = models.CharField( # 13-14 p.m
		verbose_name=_("delivery window"),
		help_text=_("Required"),
		max_length=255,
		null = True,
		blank = True,
	)
	position = models.IntegerField(
		verbose_name=_('list order'), 
		help_text=_('Required'), 
		default=0
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_deliveries',
	)

	class Meta:
		verbose_name = _('Delivery')
		verbose_name_plural = _('Deliveries')
		ordering = ['position']