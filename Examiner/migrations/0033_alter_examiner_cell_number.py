# Generated by Django 4.1.1 on 2022-12-09 08:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0032_remove_examiner_middle_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examiner',
            name='cell_Number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid Phone Number starting: 0', regex='(0\\[1-9]{9})')]),
        ),
    ]