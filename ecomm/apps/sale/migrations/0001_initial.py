# Generated by Django 4.1.7 on 2023-02-26 06:49

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import ecomm.apps.sale.models.sale


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.JSONField(max_length=500)),
                ('coupon_code', models.CharField(max_length=20, unique=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp_coupons', to='company.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('sale_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('price_override', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp_prod_sale', to='company.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prod_sale', to='product.product')),
            ],
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.JSONField()),
                ('short_desc', models.JSONField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=ecomm.apps.sale.models.sale.sale_image_upload_to)),
                ('is_showcase', models.BooleanField(default=False)),
                ('sale_reduction', models.IntegerField(default=0)),
                ('is_schedule', models.BooleanField(default=False)),
                ('sale_start', models.DateField()),
                ('sale_end', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp_sales', to='company.company')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sale_coupons', to='sale.coupon')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_creator', to=settings.AUTH_USER_MODEL)),
                ('prod_sale', models.ManyToManyField(related_name='prod_sales', through='sale.ProductSale', to='product.product')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
            managers=[
                ('objs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='productsale',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='sale.sale'),
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(fields=['slug'], name='sale_sale_slug_a3b89a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productsale',
            unique_together={('product_id', 'sale_id')},
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['coupon_code'], name='sale_coupon_coupon__4d215a_idx'),
        ),
    ]
