# Generated by Django 4.1.7 on 2023-02-26 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import ecomm.apps.brand.models.brand


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=180, unique=True, verbose_name='Brand URL')),
                ('name', models.JSONField(max_length=255)),
                ('site_url', models.CharField(blank=True, max_length=180, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.brand.models.brand.brand_logo_upload_to)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='company.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddIndex(
            model_name='brand',
            index=models.Index(fields=['slug'], name='brand_brand_slug_db538a_idx'),
        ),
    ]