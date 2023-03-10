# Generated by Django 4.1.7 on 2023-03-13 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='Account'),
        ),
    ]
