from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import gettext_lazy as _
from mptt.models import (
	MPTTModel, 
	TreeForeignKey, 
	TreeManyToManyField,
)
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
	CacheMixin,
)
Account = get_user_model()

def category_thumb_upload_to(instance, filename):
	return f'company/{instance.company}/category/thumb/{instance.slug}/{filename}'


class Category(MPTTModel, BaseModel, TimestampsMixin, SoftdeleteMixin, HelpersMixin, ImgMixin, CacheMixin):
	CACHE_KEY = 'company-{0}-categories'

	class ThumbAs(models.TextChoices):
		IMG    = 'IMG',    _('Image')
		SVG    = 'SVG',    _('Svg icon')
		HIDDEN = 'HIDDEN', _('Hidden')

	slug = models.SlugField(
		max_length=150,
		verbose_name=_('Category URL'),
		help_text=_(
			'format: required, letters, numbers, underscore, or hyphens'
		),
	)
	name = models.JSONField(
		max_length=180, 
	)
	thumb = models.ImageField(
		upload_to=category_thumb_upload_to, 
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
	parent = TreeForeignKey(
		'self',
		null=True,
		blank=True,
		on_delete=models.PROTECT,
		related_name='children',
		verbose_name=_('parent of category'),
		help_text=_('format: not required'),
	)
	position = models.IntegerField(
		default=0,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='categories',
	)

	class MPTTMeta:
		order_insertion_by = ['-created_at']

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_category_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')), # condition='TRUE'
		]

	def __str__(self):
		return self.slug

	def save(self, *args, **kwargs):
		Category.delete_cache(self.company.alias)
		super().save(*args, **kwargs)
		self.resize_img('thumb', settings.IMAGE_WIDTH['THUMBNAIL'])

	def delete(self, *args, **kwargs):
		Category.delete_cache(self.company.alias)
		super().delete(*args, **kwargs)
