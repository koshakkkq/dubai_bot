# Generated by Django 4.2.3 on 2023-07-29 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_shopregistrationcode_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='shop',
            name='lon',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='internal_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='courier',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='courier',
            name='phone',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordercredential',
            name='address',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='ordercredential',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='location',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_offers', models.BigIntegerField(default=0)),
                ('new_couriers', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.telegramuser')),
            ],
        ),
        migrations.CreateModel(
            name='ShopNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_available_orders', models.BigIntegerField(default=0)),
                ('new_active_orders', models.BigIntegerField(default=0)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shop')),
            ],
        ),
    ]
