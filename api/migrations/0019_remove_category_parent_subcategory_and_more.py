# Generated by Django 5.0.6 on 2024-08-26 06:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='api.category')),
            ],
        ),
        migrations.AddField(
            model_name='blogpage',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_pages', to='api.subcategory'),
        ),
    ]
