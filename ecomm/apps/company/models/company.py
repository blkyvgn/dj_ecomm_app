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
	CacheMixin,
)
Account = get_user_model()

def company_logo_upload_to(instance, filename):
	return f'company/{instance.alias}/logo/{filename}'

class Company(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin, CacheMixin):
	CACHE_KEY = 'company-{0}'

	alias = models.CharField(
		max_length=30, 
		unique=True,
	)
	name = models.JSONField(
		null=True, 
		blank=True,
	)
	logo = models.ImageField(
		upload_to=company_logo_upload_to, 
		null=True, 
		blank=True
	)
	options = models.JSONField(
		null=True, 
		blank=True,
	)

	def __str__(self):
		return self.alias

	class Meta:
		verbose_name =  _('Company')
		verbose_name_plural =  _('Companies')
		ordering = ('-created_at',)
		indexes = [
			models.Index(fields=['alias',]),
		]

	def save(self, *args, **kwargs):
		if self.pk:
			Company.delete_cache(self.alias)
		super().save(*args, **kwargs)
		self.resize_img('logo', settings.IMAGE_WIDTH['LOGO'])

	def delete(self, *args, **kwargs):
		Company.delete_cache(self.alias)
		super().delete(*args, **kwargs)

	@classmethod
	def get_from_cache(cls, **kwargs):
		return cls.objs.valid().filter(alias=kwargs.get('cache_key')).first()

	# @classmethod
	# def get_cache_key(cls, **kwargs):
	# 	return f'company-{kwargs.get("cache_key")}'





