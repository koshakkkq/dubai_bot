# Generated by Django 4.2.3 on 2023-07-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_order_status_alter_telegramuser_telegram_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierRegistrationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('used', models.BooleanField(default=False)),
                ('user', models.IntegerField(null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
