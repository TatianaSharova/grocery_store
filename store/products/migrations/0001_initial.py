# Generated by Django 4.2.16 on 2024-11-22 13:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Корзина пользователя',
                'verbose_name_plural': 'Корзины пользователей',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Product_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(upload_to='product_group/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Группа продуктов',
                'verbose_name_plural': 'Группы продуктов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(upload_to='type/', verbose_name='Изображение')),
                ('product_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product_group', verbose_name='группа продуктов')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг')),
                ('price', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальная цена 1')], verbose_name='Цена')),
                ('image', models.ImageField(upload_to='product/', verbose_name='Изображение')),
                ('in_stock', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0, 'Минимальное количество 0')], verbose_name='Остаток в магазине')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.type', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное количество 1')], verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Содержание корзины')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукты в корзине',
                'ordering': ('cart',),
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='products.CartProduct', to='products.product', verbose_name='Содержание корзины'),
        ),
    ]