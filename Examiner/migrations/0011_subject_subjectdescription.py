# Generated by Django 4.1.1 on 2022-10-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0010_districtcsv'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subjectDescription',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
