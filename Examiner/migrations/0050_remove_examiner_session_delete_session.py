# Generated by Django 4.1.1 on 2022-11-07 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0049_session_examiner_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examiner',
            name='session',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]