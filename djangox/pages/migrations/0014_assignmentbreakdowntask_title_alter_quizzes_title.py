# Generated by Django 4.2.9 on 2024-12-05 04:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0013_alter_moduleitems_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignmentbreakdowntask",
            name="title",
            field=models.CharField(default="Task", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="quizzes",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]