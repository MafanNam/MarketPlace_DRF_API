# Generated by Django 4.2.4 on 2023-08-08 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Seller'), (2, 'Customer')], default=2, null=True),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
