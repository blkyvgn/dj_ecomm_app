# Generated by Django 4.1.7 on 2023-03-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='full_name',
            field=models.TextField(),
        ),
    ]
