from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import get_language


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