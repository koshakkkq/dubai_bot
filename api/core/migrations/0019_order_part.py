# Generated by Django 4.2.3 on 2023-08-03 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_parttype_shop_parts'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.parttype'),
        ),
    ]
