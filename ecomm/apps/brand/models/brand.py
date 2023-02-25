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

def brand_logo_upload_to(instance, filename):
	return f'company/{instance.company.alias}/brand/logo/{filename}'

class Brand(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	slug = models.SlugField(
		max_length=180,
		unique=True,
		verbose_name=_('Brand URL'),
	)
	name = models.JSONField(
		max_length=255, 
	)
	site_url = models.CharField(
		max_length=180,
		null = True,
		blank = True,
	)
	logo = models.ImageField(
		upload_to=brand_logo_upload_to, 
		null=True, 
		blank=True
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='brand_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='brand_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='brands',
	)

	def __str__(self):
		return self.slug
		
	class Meta:
		verbose_name = _('Brand')
		verbose_name_plural = _('Brands')
		indexes = [
			models.Index(fields=['slug',]),
		]

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.resize_img('logo', settings.IMAGE_WIDTH['LOGO'])

	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)

	