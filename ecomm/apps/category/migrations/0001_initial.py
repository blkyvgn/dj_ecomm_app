# Generated by Django 4.1.7 on 2023-02-24 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ecomm.apps.category.models.category
import ecomm.vendors.mixins.model
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0003_alter_company_options_company_id_alter_company_alias'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscore, or hyphens', max_length=150, unique=True, verbose_name='Category URL')),
                ('name', models.JSONField(max_length=180)),
                ('thumb', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.category.models.category.category_thumb_upload_to)),
                ('order', models.IntegerField(default=0)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='company.company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='format: not required', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='category.category', verbose_name='parent of category')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model, ecomm.vendors.mixins.model.CacheMixin),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['slug'], name='category_ca_slug_6890c5_idx'),
        ),
    ]