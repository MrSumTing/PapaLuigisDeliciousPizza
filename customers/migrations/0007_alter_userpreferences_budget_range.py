# Generated by Django 5.1.1 on 2024-10-09 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_userpreferences_budget_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='budget_range',
            field=models.FloatField(default=7.0),
        ),
    ]
