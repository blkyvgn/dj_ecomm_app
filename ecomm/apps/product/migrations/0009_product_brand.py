# Generated by Django 4.1.7 on 2023-02-25 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0002_alter_brand_name'),
        ('product', '0008_alter_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod', to='brand.brand'),
        ),
    ]
