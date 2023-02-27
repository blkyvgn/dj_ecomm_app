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
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
)
Account = get_user_model()

def sale_image_upload_to(instance, filename):
	return f'company/{instance.company.alias}/sale/image/{filename}'

class Sale(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	slug = models.SlugField(
		max_length=255, 
	)
	name = models.JSONField()
	short_desc = models.JSONField()
	image = models.ImageField(
		upload_to=sale_image_upload_to, 
		null=True, 
		blank=True
	)
	is_showcase = models.BooleanField(
		default=False,
	)
	sale_reduction = models.IntegerField(
		default=0
	)
	is_schedule = models.BooleanField(
		default=False
	)
	sale_start = models.DateField()
	sale_end = models.DateField()
	coupon = models.ForeignKey(
		'Coupon',
		related_name='sale_coupons',
		on_delete=models.PROTECT,
		null=True,
		blank=True,
	)
	prod_sale = models.ManyToManyField(
		'product.Product',
		related_name='prod_sales',
		through='ProductSale',
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_sales',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Sale')
		verbose_name_plural = _('Sales')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_sale_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')), # condition='TRUE'
		]

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.resize_img('image', settings.IMAGE_WIDTH['SLIDER'])

	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)

	def clean(self):
		if self.sale_start > self.sale_end:
			raise ValidationError(_('End data before the start date'))

class ProductSale(BaseModel, TimestampsMixin):
	product = models.ForeignKey(
		'product.Product',
		related_name='prod_sale',
		on_delete=models.PROTECT,
	)
	sale = models.ForeignKey(
		Sale,
		related_name='sale',
		on_delete=models.CASCADE,
	)
	sale_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		default=Decimal('0.00'),
		validators=[
			MinValueValidator(Decimal('0.00')),
		],
	)
	price_override = models.BooleanField(
		default=False,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_prod_sale',
	)

	class Meta:
		unique_together = (('product_id', 'sale_id'),)
	