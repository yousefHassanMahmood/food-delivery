# Generated by Django 5.2.3 on 2025-06-28 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('image_url', models.URLField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=255)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('OutForDelivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('avg_rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Customer'), (2, 'Restaurant')], default=1, help_text='1 = Customer, 2 = Restaurant')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.restaurant'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='core.restaurant'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.user')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='core.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.user'),
        ),
    ]
