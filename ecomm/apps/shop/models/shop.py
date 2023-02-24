# from django.db import models
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from ecomm.vendors.base.model import BaseModel
# from django.utils.translation import gettext_lazy as _
# from ecomm.vendors.mixins.model import (
# 	SoftdeleteMixin, 
# 	TimestampsMixin,
# 	ImgMixin,
# 	HelpersMixin,
# )
# Account = get_user_model()


# class Shop(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
# 	alias = models.CharField(
# 		max_length=30, 
# 		primary_key=True
# 	)
# 	options = models.JSONField(
# 		null=True, 
# 		blank=True,
# 	)
# 	company = models.OneToOneField(
# 		'company.Company', 
# 		on_delete=models.CASCADE,
# 	)

# 	def __str__(self):
# 		return self.pk

# 	class Meta:
# 		verbose_name =  _('Shop')
# 		verbose_name_plural =  _('Shops')

# 	def save(self, *args, **kwargs):
# 		self.alias = self.company.alias
# 		super().save(*args, **kwargs)






