# Generated by Django 4.1.7 on 2023-03-13 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_rename_line_address_address_line_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
