# Generated by Django 4.1.7 on 2023-02-24 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_media_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='is_feature',
            new_name='is_showcase',
        ),
    ]