# Generated by Django 5.0.6 on 2024-07-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_merge_20240722_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='text',
            field=models.CharField(blank=True, max_length=30000),
        ),
    ]
