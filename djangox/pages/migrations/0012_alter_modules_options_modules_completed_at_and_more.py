# Generated by Django 4.2.9 on 2024-12-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0011_remove_assignmentfile_thumbnail_modules_moduleitems"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="modules",
            options={
                "ordering": ["position"],
                "verbose_name": "Module",
                "verbose_name_plural": "Modules",
            },
        ),
        migrations.AddField(
            model_name="modules",
            name="completed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="modules",
            name="items_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="modules",
            name="published",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="modules",
            name="state",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="modules",
            name="workflow_state",
            field=models.CharField(default="active", max_length=50),
        ),
    ]
