# Generated by Django 5.1.7 on 2025-03-26 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0003_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='task_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='task_tracker.task'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_comment',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(blank=True, choices=[('p', 'Production'), ('n', 'Non-production')], default='p', max_length=1),
        ),
    ]
