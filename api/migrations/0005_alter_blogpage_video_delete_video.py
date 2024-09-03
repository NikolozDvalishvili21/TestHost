# Generated by Django 5.0.6 on 2024-07-06 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_video_blogpage_video'),
        ('wagtailvideos', '0015_video_height_video_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='v', to='wagtailvideos.video'),
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
