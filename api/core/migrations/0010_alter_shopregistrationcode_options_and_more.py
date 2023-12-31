# Generated by Django 4.2.3 on 2023-07-24 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_courierregistrationcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopregistrationcode',
            options={'verbose_name': 'Shop invite code.', 'verbose_name_plural': 'Shop invite codes.'},
        ),
        migrations.AlterField(
            model_name='courierfeedback',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='offer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.orderoffer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Pending.'), (1, 'Active.'), (2, 'Done.'), (3, 'Canceled.')], default=0),
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='raiting',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1),
        ),
    ]
