# Generated by Django 5.1.1 on 2024-10-16 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_order_estimated_delivery_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set(),
        ),
    ]
