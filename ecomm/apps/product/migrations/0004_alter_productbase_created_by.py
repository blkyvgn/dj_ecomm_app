# Generated by Django 4.1.7 on 2023-02-24 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_productattribute_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbase',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_base_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
