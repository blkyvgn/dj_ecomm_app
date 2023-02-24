from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now
from django.templatetags.static import static
from django.utils.translation import get_language
from ecomm.vendors.helpers.image import resize_image
from django.utils.translation import gettext_lazy as _


class SoftdeleteMixin(models.Model):
	deleted_at = models.DateTimeField(
		null=True, 
		blank=True
	)

	class Meta:
		abstract = True


class TimestampsMixin(models.Model):
	created_at = models.DateTimeField(
		default = now,
		editable=False
	)
	updated_at = models.DateTimeField(
		null=True, 
		blank=True
	)

	class Meta:
		abstract = True


class MetaDataMixin(models.Model):
	meta_keywords = models.CharField(
		max_length=255,
		null=True, 
		blank=True
	)
	meta_description = models.CharField(
		max_length=255, 
		null=True, 
		blank=True
	)
	# meta_author = models.CharField(
	# 	max_length=255, 
	# 	null=True, 
	# 	default='',
	# )
	
	class Meta:
		abstract = True


class HelpersMixin(models.Model):
	@property
	def name_in_lang_or_default(self, lang_key=get_language()):
		try:
			name = self.name.get(lang_key, self.name.get(settings.LANGUAGE_CODE, None))
		except:
			name = None
		return name

	class Meta:
		abstract = True


class ImgMixin(models.Model):
	
	def resize_img(self, img_name, width):
		img = getattr(self, img_name)
		if img:
			new_img = resize_image(img.path, width)
			if new_img:
				new_img.save(img.path)

	def img_url_or_default(self, img_name, default=settings.DEFAULT_IMAGE['PLACEHOLDER']):
		img = getattr(self, img_name)
		try:
			url = img.url
		except:
			url = static(default)
		return url

	class Meta:
		abstract = True


class CacheMixin():
	''' Set CACHE_KEY format str in class 
		or add classmethods get_cache_key(cls, **kwargs): return full cache key,
		get_from_cache_or_set(cls, **kwargs): return result of query '''
	@classmethod
	def get_full_cache_key(cls, cache_key=None):
		if hasattr(cls, 'CACHE_KEY'):
			full_cache_key = cls.CACHE_KEY.format(str(cache_key) if cache_key else '')
		elif hasattr(cls, 'get_cache_key'):
			full_cache_key = cls.get_cache_key(cache_key=cache_key)
		else:
			if not cache_key:
				raise ValueError('full_cache_key cannot be None')
			full_cache_key = cache_key
		return full_cache_key

	@classmethod
	def get_from_cache_or_set(cls, cache_key=None, query_set=False, timeout=settings.CACHE_TIMEOUT['FIVE_MINUTES']):
		full_cache_key = cls.get_full_cache_key(cache_key)

		res = cache.get(full_cache_key, None)
		if not res:
			if query_set == False and not hasattr(cls, 'get_from_cache_query'):
				raise ValueError('query_set cannot be None')

			if query_set != False:
				res = query_set
			elif hasattr(cls, 'get_from_cache_query'):
				res = cls.get_from_cache(cache_key=cache_key)
			else:
				raise ValueError('query_set cannot be None')

			if res:
				cache.set(full_cache_key, res, timeout=timeout)
		return res

	@classmethod
	def delete_cache(cls, cache_key=None):
		full_cache_key = cls.get_full_cache_key(cache_key)
		cache.delete(full_cache_key)

	class Meta:
		abstract = True

