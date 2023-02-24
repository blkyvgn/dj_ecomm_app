# Generated by Django 4.1.7 on 2023-02-24 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]