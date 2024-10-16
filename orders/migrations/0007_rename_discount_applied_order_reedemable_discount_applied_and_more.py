# Generated by Django 5.1.1 on 2024-10-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_order_date_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='discount_applied',
            new_name='reedemable_discount_applied',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='loyalty_discount_applied',
            field=models.BooleanField(default=False),
        ),
    ]
