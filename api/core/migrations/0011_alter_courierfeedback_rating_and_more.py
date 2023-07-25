

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_shopregistrationcode_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierfeedback',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
        migrations.AlterField(
            model_name='ordercredential',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='raiting',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
        ),
        migrations.CreateModel(
            name='CourierOrdersBlacklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.telegramuser')),
            ],
        ),
    ]
