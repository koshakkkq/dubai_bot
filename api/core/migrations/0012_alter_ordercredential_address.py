# Generated by Django 4.2.3 on 2023-07-24 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_courierfeedback_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercredential',
            name='address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
