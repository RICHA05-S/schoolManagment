# Generated by Django 3.2.7 on 2021-09-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_marks_marks_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='total_marks',
            field=models.CharField(max_length=3),
        ),
    ]
