# Generated by Django 4.1.7 on 2023-02-28 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_category_category_ca_slug_6890c5_idx_and_more'),
        ('product', '0002_remove_product_product_pro_slug_6278ef_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod_types', to='category.category'),
        ),
    ]
