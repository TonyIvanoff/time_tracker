# Generated by Django 5.1.7 on 2025-03-26 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0004_alter_comment_options_remove_comment_task_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='task_tracker.task'),
        ),
    ]
