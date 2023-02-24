# Generated by Django 4.1.7 on 2023-02-24 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='thumb_type',
            field=models.CharField(choices=[('IMG', 'Image'), ('SVG', 'Svg icon'), ('HIDDEN', 'Hidden')], default='IMG', max_length=15, verbose_name='Thumbnail type'),
        ),
    ]
