# Generated by Django 4.1.2 on 2024-07-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0008_rename_stock_compra_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
