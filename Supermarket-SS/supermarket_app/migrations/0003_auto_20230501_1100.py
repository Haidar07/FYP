# Generated by Django 3.2.8 on 2023-05-01 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket_app', '0002_auto_20230430_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='supermarket_app.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default='3'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supermarket_app.cart')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='supermarket_app.product')),
            ],
        ),
    ]
