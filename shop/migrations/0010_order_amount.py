# Generated by Django 5.1 on 2024-09-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_orderupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]