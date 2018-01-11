# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-09 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('papermanager', '0010_auto_20180107_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publishedDate', models.DateTimeField(auto_now_add=True)),
                ('whitePaper', models.FileField(upload_to='uploads/%Y-%m-%d/')),
                ('paper', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='papermanager.Paper')),
            ],
        ),
    ]