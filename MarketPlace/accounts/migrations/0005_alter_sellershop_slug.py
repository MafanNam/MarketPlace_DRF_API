# Generated by Django 4.2.4 on 2023-08-20 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_sellershop_email_alter_sellershop_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellershop',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]