# Generated by Django 4.2.4 on 2023-08-22 15:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, unique=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(default='static/images/default/default_project.png', upload_to=store.models.get_upload_path_main_product_image)),
                ('link_youtube', models.URLField(blank=True)),
                ('article', models.CharField(db_index=True, max_length=50, unique=True)),
                ('price_new', models.PositiveIntegerField()),
                ('price_old', models.PositiveIntegerField(blank=True, default=0)),
                ('stock_qty', models.PositiveIntegerField()),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('numReviews', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attribute_value', models.ManyToManyField(to='store.attributevalue')),
                ('brand', models.ForeignKey(blank=True, on_delete=models.SET('non brand'), to='store.brand')),
                ('category', models.ForeignKey(blank=True, on_delete=models.SET('non category'), to='store.category')),
                ('seller_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.sellershop')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, max_length=500)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='static/images/default/default_project.png', upload_to=store.models.get_upload_path_product_image)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
        ),
    ]
