# Generated by Django 3.1.7 on 2021-04-06 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0012_auto_20210405_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]