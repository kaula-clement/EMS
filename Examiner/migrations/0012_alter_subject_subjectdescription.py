# Generated by Django 4.1.1 on 2022-10-04 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0011_subject_subjectdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subjectDescription',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
