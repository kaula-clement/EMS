# Generated by Django 4.1.1 on 2022-11-21 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0014_eczstaff_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'EAD'), (2, 'Staff'), (3, 'Examiner'), (4, 'Station-Admin')], default=1),
        ),
    ]
