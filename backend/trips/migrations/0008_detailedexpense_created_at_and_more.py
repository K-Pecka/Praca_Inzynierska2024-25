# Generated by Django 5.1.7 on 2025-05-28 13:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_remove_detailedexpense_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailedexpense',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailedexpense',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
