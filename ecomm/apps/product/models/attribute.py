from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
)
Account = get_user_model()

def prod_attribut_thumb_upload_to(instance, filename):
	return f'company/{instance.company}/prod_attribut/thumb/{instance.slug}/{filename}'

class ProductAttribute(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	class ThumbAs(models.TextChoices):
		IMG    = 'IMG',    _('Image')
		SVG    = 'SVG',    _('Svg icon')
		HIDDEN = 'HIDDEN', _('Hidden')

	slug = models.SlugField(
		max_length=255,
	)
	thumb = models.ImageField(
		upload_to=prod_attribut_thumb_upload_to, 
		null=True, 
		blank=True,
	)
	svg = models.TextField(
		null=True, 
		blank=True,
	)
	thumb_as = models.CharField(
		max_length=15,
		choices=ThumbAs.choices,
		default=ThumbAs.HIDDEN,
		verbose_name=(_('Thumbnail as'))
	)
	name = models.JSONField(
		null=True, 
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='prod_attributes',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Product attribute')
		verbose_name_plural = _('Product attributes')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_attribute_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')), # condition='TRUE'
		]


class ProductAttributeValue(BaseModel, HelpersMixin):
	product_attribute = models.ForeignKey(
		ProductAttribute,
		related_name='values',
		on_delete=models.PROTECT,
	)
	value = models.CharField(
		max_length=255,
	)
	name = models.JSONField(
		null=True, 
		blank=True,
	)

	def __str__(self):
		return f'{self.product_attribute} ({self.value})'


class ProductAttributeValues(BaseModel):
	attribute_values = models.ForeignKey(
		ProductAttributeValue,
		related_name='values',
		on_delete=models.PROTECT,
	)
	product = models.ForeignKey(
		'Product',
		related_name='attr_values',
		on_delete=models.PROTECT,
	)

	class Meta:
		unique_together = (('attribute_values', 'product'),)