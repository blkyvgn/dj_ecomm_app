from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
Account = get_user_model()

def profile_photo_upload_to(instance, filename):
	return f'account/{instance.id}/photo/{filename}'

class Profile(models.Model):
	class Sex(models.TextChoices):
		MALE      = 'MALE', _('Male')
		FEMALE    = 'FEMALE', _('Female')

	first_name = models.CharField(
		max_length=20, 
	)
	middle_name = models.CharField(
		max_length=20, 
		null=True, 
		blank=True,
	)
	last_name = models.CharField(
		max_length=20, 
	)
	photo = models.ImageField(
		upload_to=profile_photo_upload_to, 
		null=True, 
		blank=True
	)
	phone = models.CharField(
		max_length=25, 
		null=True, 
		blank=True
	)
	age = models.IntegerField(
		null=True, 
		blank=True
	)
	birthdate = models.DateField(
		null=True, 
		blank=True
	)
	sex = models.CharField(
		max_length=8, 
		choices=Sex.choices,
		default=Sex.MALE,
	)
	account = models.OneToOneField(
		Account, 
		on_delete=models.CASCADE
	)

	@property
	def full_name(self):
		return f'{self.first_name} {self.middle_name} {self.last_name}'

	@full_name.setter
	def full_name(self, val):
		first, *middle, last = val.split(' ')
		self.first_name = first
		self.middle_name = ' '.join(middle) if middle.len > 0 else None
		self.last_name = last

	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _('Profiles')