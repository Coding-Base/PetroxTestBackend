# Generated by Django 5.1.5 on 2025-02-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsession',
            name='duration',
            field=models.IntegerField(default=300),
        ),
    ]
