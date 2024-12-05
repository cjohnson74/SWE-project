# Generated by Django 4.2.9 on 2024-11-21 05:21
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0003_rename_break_and_buffer_assignmentbreakdown_breaks_and_buffer"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="completion_reward",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="complexity_evaluation",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="complexity_scores",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="focus_impprovement",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="initial_assessment",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="key_requirements",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="milestone_rewards",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="motivation_boosters",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="potential_challenges",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="progress_tracking",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="progress_visualization",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="reasoning",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="skill_level_considerations",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdown",
            name="time_management",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentbreakdowntask",
            name="potential_distractions",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="assignmentbreakdowntask",
            name="focus_techniques",
            field=models.TextField(blank=True, null=True),
        ),
    ]