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

def prod_type_thumb_upload_to(instance, filename):
	return f'company/{instance.company}/prod_type/thumb/{instance.slug}/{filename}'

class ProductType(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	class ThumbAs(models.TextChoices):
		IMG    = 'IMG',    _('Image')
		SVG    = 'SVG',    _('Svg icon')
		HIDDEN = 'HIDDEN', _('Hidden')

	slug = models.SlugField(
		max_length=255,
	)
	thumb = models.ImageField(
		upload_to=prod_type_thumb_upload_to, 
		null=True, 
		blank=True
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
	name = models.JSONField()
	category = models.ForeignKey(
		'category.Category',
		related_name='types',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	product_type_attributes = models.ManyToManyField(
		'ProductAttribute',
		related_name='types',
		through='ProductTypeAttribute',
	)
	in_menu = models.BooleanField(
		default = False,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='prod_types',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Product type')
		verbose_name_plural = _('Product types')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_prod_type_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')), # condition='TRUE'
		]



class ProductTypeAttribute(BaseModel):
	prod_attribute = models.ForeignKey(
		'ProductAttribute',
		related_name='attribute',
		on_delete=models.PROTECT,
	)
	prod_type = models.ForeignKey(
		ProductType,
		related_name='type',
		on_delete=models.PROTECT,
	)
