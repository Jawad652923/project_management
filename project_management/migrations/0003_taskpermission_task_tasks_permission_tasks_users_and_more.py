# Generated by Django 5.0.6 on 2024-06-27 23:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0002_projects_permission_alter_tasks_project_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpermission',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.tasks'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='permission',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='tasks',
            name='users',
            field=models.ManyToManyField(related_name='user_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskpermission',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projects'),
        ),
    ]
