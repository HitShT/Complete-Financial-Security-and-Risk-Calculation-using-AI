# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-02-23 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0006_auto_20210224_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentfinancialmodel',
            name='assets_name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='presentfinancialmodel',
            name='assets_valuation',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='presentfinancialmodel',
            name='liabilities_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='presentfinancialmodel',
            name='liabilities_valuation',
            field=models.FloatField(default=0),
        ),
    ]
