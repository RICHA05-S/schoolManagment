# Generated by Django 3.2.7 on 2021-09-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210909_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')], default='Student', max_length=10),
        ),
    ]