# Generated by Django 4.2.9 on 2024-11-25 07:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0009_assignmentfile_claude_response"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignmentfile",
            name="chunk_embeddings",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentfile",
            name="embedding_vector",
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assignmentfile",
            name="last_embedded",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
