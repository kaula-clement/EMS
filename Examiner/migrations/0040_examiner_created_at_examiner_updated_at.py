# Generated by Django 4.1.1 on 2022-11-01 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0039_alter_examiner_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='examiner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examiner',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]