# Generated by Django 4.1.7 on 2023-03-13 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_default_address_is_default'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='line',
            new_name='address_line',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]