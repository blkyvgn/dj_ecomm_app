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

	def company(self, cmp_id=None):
		return self.filter(company_id=cmp_id)

	def filter_by_params(self, _or=False, **kwargs):
		if kwargs:
			_q = Q()
			conn = Q.AND if not _or else Q.OR
			for key, val in kwargs.items():
				filter_dict = {key: val}
				_q.add(Q(**filter_dict), conn)
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

	def company(self, cmp_id=None):
		return self.get_queryset().company(cmp_id)

	def filter_by_params(self, _or=False, **kwargs):
		return self.get_queryset().filter_by_params(_or, **kwargs)

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

	@classmethod
	def get_first_by_filters(cls, _or=False, **kwargs):
		return cls.objs.filter_by_params(_or, **kwargs).first()


class EmptyBaseModel(models.Model):
	class Meta:
		abstract = True

class AdminBaseModel(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE