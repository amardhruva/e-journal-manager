# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-06 11:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('papermanager', '0007_paper_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='reviewer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reveiwpaper', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paperversion',
            name='submissionType',
            field=models.CharField(choices=[('latex', 'Lamport TeX (LaTeX)'), ('pdf', 'Portable Document Format (PDF)')], default='pdf', max_length=7),
        ),
    ]