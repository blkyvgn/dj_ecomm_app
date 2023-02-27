from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ecomm.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
	MinValueValidator,
	MaxValueValidator,
)
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
	MetaDataMixin,
)
from django.db.models import (
	F, 
	Count,
)
Account = get_user_model()


class ProductBase(BaseModel, TimestampsMixin, SoftdeleteMixin, HelpersMixin):
	slug = models.SlugField(
		max_length=180,
		unique=True,
		verbose_name=_('Product(base) URL'),
	)
	name = models.JSONField()
	short_desc = models.JSONField(
		null=True, 
		blank=True,
	)
	category = models.ForeignKey(
		'category.Category',
		related_name='base_prods',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_base_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_base_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_base_prods',
	)

	class Meta:
		verbose_name = _('Base product')
		verbose_name_plural = _('Base products')
		indexes = [
			models.Index(fields=['slug',]),
		]

	def __str__(self):
		return self.slug


class ProductBaseTranslation(MetaDataMixin):
	lang = models.CharField(
		max_length=5, 
		default = settings.LANGUAGE_CODE,
	)
	description = models.TextField(
		null=True, 
		blank=True
	)
	prod_base = models.ForeignKey(
		ProductBase, 
		related_name='translation', 
		on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = _('Base product translation')
		verbose_name_plural = _('Base product translations')



def product_thumb_upload_to(instance, filename):
	return f'company/{instance.company.alias}/product/{instance.slug}/thumb/{filename}'


class Product(BaseModel, TimestampsMixin, SoftdeleteMixin, HelpersMixin, ImgMixin):
	slug = models.SlugField(
		max_length=255,
		unique=True,
		verbose_name=_('Product URL'),
	)
	sku = models.CharField(
		max_length=20,
		unique=True,
	)
	thumb = models.ImageField(
		upload_to=product_thumb_upload_to, 
		null=True, 
		blank=True
	)
	# extension for name - red,small etc. ({'en':['red', 'small']}) 
	ext_name = models.JSONField( 
		default = dict,
		blank=True,
		null=True,
	)
	full_name = models.CharField(
		max_length=500,
	)
	prod_base = models.ForeignKey(
		ProductBase, 
		related_name='base_prods', 
		on_delete=models.CASCADE
	)
	brand = models.ForeignKey(
		'brand.Brand',
		related_name='prod',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
	)
	product_type = models.ForeignKey(
		'ProductType', 
		related_name='prod', 
		on_delete=models.PROTECT
	)
	attribute_values = models.ManyToManyField(
		'ProductAttributeValue',
		related_name='prods',
		through='ProductAttributeValues',
	)
	is_default = models.BooleanField(
		default=False,
	)
	price = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		validators=[
			MinValueValidator(settings.MIN_PRICE),
			MaxValueValidator(settings.MAX_PRICE),
		]
	)
	sale_price = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		blank=True,
		null=True,
		validators=[
			MinValueValidator(settings.MIN_PRICE),
			MaxValueValidator(settings.MAX_PRICE),
		],
	)
	is_digital = models.BooleanField(
		default=False,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_prods',
	)

	def __str__(self):
		return f'{self.slug}|{self.sku}'

	class Meta:
		verbose_name = _('Product')
		verbose_name_plural = _('Products')
		ordering = ('-created_at',)
		indexes = [
			models.Index(fields=['slug', 'sku',]),
		]

	def get_full_name(self):
		ext_name = self.ext_name.values() if self.ext_name else []
		_full_name = [*self.prod_base.name.values(), *ext_name]
		return '@'.join(_full_name)

	@property
	def ext_name_in_lang_or_default(self, lang_key=get_language()):
		try:
			ext_name = self.ext_name.get(lang_key, self.ext_name.get(settings.LANGUAGE_CODE, None))
		except:
			ext_name = None
		return ext_name

	def save(self, *args, **kwargs):
		self.full_name = self.get_full_name()
		super().save(*args, **kwargs)
		self.resize_img('thumb', settings.IMAGE_WIDTH['SHOWCASE'])

	@classmethod
	def get_popular(cls, company_id, per_page):
		return cls.objs.valid().company(company_id).\
			annotate(sold=F('stock_prod__units_sold')).\
			select_related('prod_base').order_by('-sold')[:per_page]


