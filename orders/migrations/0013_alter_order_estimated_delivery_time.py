# Generated by Django 5.1.1 on 2024-10-15 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estimated_delivery_time',
            field=models.IntegerField(blank=True, default=30, null=True),
        ),
    ]
