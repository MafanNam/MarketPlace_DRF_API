# Generated by Django 4.2.4 on 2023-08-25 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_item',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='sub_total',
        ),
    ]
