# Generated by Django 4.2.3 on 2023-07-22 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_order_product_alter_orderoffer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Active.'), (1, 'Pending.'), (2, 'Done.'), (3, 'Canceled.')], default=0),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.IntegerField(db_index=True),
        ),
    ]