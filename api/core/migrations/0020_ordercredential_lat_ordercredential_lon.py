# Generated by Django 4.2.3 on 2023-08-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_order_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercredential',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ordercredential',
            name='lon',
            field=models.FloatField(default=0),
        ),
    ]