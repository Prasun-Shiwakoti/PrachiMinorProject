# Generated by Django 5.0.1 on 2024-02-09 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_subject_credit_hours_teacher_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='faculty',
        ),
        migrations.AddField(
            model_name='subject',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.faculty'),
            preserve_default=False,
        ),
    ]
