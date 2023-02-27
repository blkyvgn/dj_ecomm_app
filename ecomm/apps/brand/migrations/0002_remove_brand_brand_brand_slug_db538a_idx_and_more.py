# Generated by Django 4.1.7 on 2023-02-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='brand',
            name='brand_brand_slug_db538a_idx',
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=180, verbose_name='Brand URL'),
        ),
        migrations.AddIndex(
            model_name='brand',
            index=models.Index(fields=['company_id', 'slug'], name='brand_brand_company_2df763_idx'),
        ),
        migrations.AddConstraint(
            model_name='brand',
            constraint=models.UniqueConstraint(fields=('company_id', 'slug'), name='unique_brand_slug'),
        ),
    ]
