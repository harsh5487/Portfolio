# Generated by Django 2.2.2 on 2019-06-27 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_portfolio', '0009_auto_20190627_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='sell_quant',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_quant',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
