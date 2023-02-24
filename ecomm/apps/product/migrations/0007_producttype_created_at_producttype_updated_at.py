# Generated by Django 4.1.7 on 2023-02-24 17:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_is_feature_media_is_showcase'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='producttype',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
