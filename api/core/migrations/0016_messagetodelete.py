# Generated by Django 4.2.3 on 2023-07-29 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_shop_lat_shop_lon_alter_carbrand_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageToDelete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.BigIntegerField()),
                ('msg_id', models.BigIntegerField(default=None, null=True)),
            ],
        ),
    ]
