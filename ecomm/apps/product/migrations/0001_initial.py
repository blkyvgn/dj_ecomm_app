# Generated by Django 4.1.7 on 2023-02-26 06:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import ecomm.apps.product.models.attribute
import ecomm.apps.product.models.media
import ecomm.apps.product.models.prod_type
import ecomm.apps.product.models.product


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('brand', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Product URL')),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('thumb', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.product.models.product.product_thumb_upload_to)),
                ('ext_name', models.JSONField(blank=True, default=dict, null=True)),
                ('full_name', models.CharField(max_length=500)),
                ('is_default', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(1000000)])),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(1000000)])),
                ('is_digital', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('thumb', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.product.models.attribute.prod_attribut_thumb_upload_to)),
                ('svg', models.TextField(blank=True, null=True)),
                ('thumb_as', models.CharField(choices=[('IMG', 'Image'), ('SVG', 'Svg icon'), ('HIDDEN', 'Hidden')], default='HIDDEN', max_length=15, verbose_name='Thumbnail as')),
                ('name', models.JSONField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_attributes', to='company.company')),
            ],
            options={
                'verbose_name': 'Product attribute',
                'verbose_name_plural': 'Product attributes',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('value', models.CharField(max_length=255)),
                ('name', models.JSONField(blank=True, null=True)),
                ('product_attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='values', to='product.productattribute')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=180, unique=True, verbose_name='Product(base) URL')),
                ('name', models.JSONField()),
                ('short_desc', models.JSONField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_prods', to='category.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp_base_prods', to='company.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_base_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_base_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Base product',
                'verbose_name_plural': 'Base products',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('thumb', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.product.models.prod_type.prod_type_thumb_upload_to)),
                ('svg', models.TextField(blank=True, null=True)),
                ('thumb_as', models.CharField(choices=[('IMG', 'Image'), ('SVG', 'Svg icon'), ('HIDDEN', 'Hidden')], default='HIDDEN', max_length=15, verbose_name='Thumbnail as')),
                ('name', models.JSONField()),
                ('in_menu', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='types', to='category.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_types', to='company.company')),
            ],
            options={
                'verbose_name': 'Product type',
                'verbose_name_plural': 'Product types',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductTypeAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('prod_attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attribute', to='product.productattribute')),
                ('prod_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='type', to='product.producttype')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='producttype',
            name='product_type_attributes',
            field=models.ManyToManyField(related_name='types', through='product.ProductTypeAttribute', to='product.productattribute'),
        ),
        migrations.CreateModel(
            name='ProductBaseTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True)),
                ('lang', models.CharField(default='en', max_length=5)),
                ('description', models.TextField(blank=True, null=True)),
                ('prod_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='product.productbase')),
            ],
            options={
                'verbose_name': 'Base product translation',
                'verbose_name_plural': 'Base product translations',
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('attribute_values', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='values', to='product.productattributevalue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attr_values', to='product.product')),
            ],
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='attribute_values',
            field=models.ManyToManyField(related_name='prods', through='product.ProductAttributeValues', to='product.productattributevalue'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod', to='brand.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp_prods', to='company.company'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_prods', to='product.productbase'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prod', to='product.producttype'),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.product.models.media.product_media_upload_to)),
                ('alt', models.JSONField(blank=True, max_length=80, null=True)),
                ('is_showcase', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comp_media', to='company.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='media', to='product.product')),
            ],
            options={
                'verbose_name': 'Product image',
                'verbose_name_plural': 'Product images',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddIndex(
            model_name='producttype',
            index=models.Index(fields=['slug'], name='product_pro_slug_0a3c49_idx'),
        ),
        migrations.AddIndex(
            model_name='productbase',
            index=models.Index(fields=['slug'], name='product_pro_slug_aa13d2_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productattributevalues',
            unique_together={('attribute_values', 'product')},
        ),
        migrations.AddIndex(
            model_name='productattribute',
            index=models.Index(fields=['slug'], name='product_pro_slug_a99d04_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['slug', 'sku'], name='product_pro_slug_6278ef_idx'),
        ),
    ]
