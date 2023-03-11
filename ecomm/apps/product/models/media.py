from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.mixins.model import (
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
)
Account = get_user_model()

def product_media_upload_to(instance, filename):
	return f'company/{instance.product.company.alias}/product/{instance.product.slug}/media/{filename}'

class Media(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	image = models.ImageField(
		upload_to=product_media_upload_to,
		null=True, 
		blank=True,
	)
	alt = models.JSONField(
		max_length=80, 
		null=True, 
		blank=True,
	)
	is_showcase = models.BooleanField(
		default=False,
	)
	product = models.ForeignKey(
		'Product',
		on_delete=models.PROTECT,
		related_name='media',
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_media',
		null=True, 
		blank=True,
	)

	class Meta:
		verbose_name = _('Product image')
		verbose_name_plural = _('Product images')

	@property
	def alt_in_lang_or_default(self, lang_key=get_language()):
		try:
			alt = self.alt.get(lang_key, self.alt.get(settings.LANGUAGE_CODE, None))
		except:
			alt = None
		return alt

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		width = settings.IMAGE_WIDTH['SHOWCASE'] if self.is_showcase else settings.IMAGE_WIDTH['SLIDER'] 
		self.resize_img('image', width)