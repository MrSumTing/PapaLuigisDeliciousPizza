# Generated by Django 5.1.1 on 2024-10-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='order_id',
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='pizza_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
