# Generated by Django 4.1.7 on 2023-02-27 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='coupon',
            name='sale_coupon_coupon__4d215a_idx',
        ),
        migrations.RemoveIndex(
            model_name='sale',
            name='sale_sale_slug_a3b89a_idx',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sale',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['company_id', 'coupon_code'], name='sale_coupon_company_07f80b_idx'),
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(fields=['company_id', 'slug'], name='sale_sale_company_5a09e9_idx'),
        ),
        migrations.AddConstraint(
            model_name='coupon',
            constraint=models.UniqueConstraint(fields=('company_id', 'coupon_code'), name='unique_coupon_code_slug'),
        ),
        migrations.AddConstraint(
            model_name='sale',
            constraint=models.UniqueConstraint(fields=('company_id', 'slug'), name='unique_sale_slug'),
        ),
    ]