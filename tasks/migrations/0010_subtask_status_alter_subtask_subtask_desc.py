# Generated by Django 4.2.11 on 2024-05-02 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0009_remove_subtask_parent_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="subtask",
            name="status",
            field=models.IntegerField(
                choices=[(0, "Incomplete"), (1, "Completed")], default=0
            ),
        ),
        migrations.AlterField(
            model_name="subtask",
            name="subtask_desc",
            field=models.CharField(
                max_length=65, validators=[django.core.validators.MinLengthValidator(4)]
            ),
        ),
    ]