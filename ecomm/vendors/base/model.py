import logging
from django.db import models
from django.contrib import admin
from django.db.models import Prefetch
from django.db.models import Q
from django.conf import settings



class BaseQuerySet(models.QuerySet):
	def blocked(self, blocked=True):
		return self.filter(is_blocked=blocked)

	def valid(self, valid=True):
		return self.filter(is_valid=valid)

	def shop(self, id):
		return self.filter(shop_id=id)

	def filter_by_params(self, keys_params={}, _or=False):
		if keys_params:
			_q = Q()
			conn = Q.AND if not _or else Q.OR
			for key, val in keys_params.items():
				search_dict = {key: value}
				_q.add(Q(**search_dict), conn)
			return self.filter(_q)
		else:
			return self

	def by_raw(self, query_str, params):
		return self.raw(query_str, params)


class BaseManager(models.Manager):
	def get_queryset(self):
		return BaseQuerySet(self.model, using=self._db)

	def valid(self, valid=True):
		return self.get_queryset().valid(valid)

	def shop(self, id):
		return self.get_queryset().shop(id)

	def filter_by_params(self, keys_params={}, _or=False):
		return self.get_queryset().filter_by_params(keys_params, _or)

	def by_raw(self, query_str, params):
		return self.get_queryset().by_raw(query_str, params)


class BaseModel(models.Model):
	is_valid = models.BooleanField(
		default=True
	)

	objs = BaseManager()
	objects = models.Manager()
	
	class Meta:
		abstract = True


class AdminBaseModel(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE