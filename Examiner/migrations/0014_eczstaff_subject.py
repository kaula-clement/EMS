# Generated by Django 4.1.1 on 2022-11-18 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0013_remove_eczstaff_to_province_eczstaff_paper'),
    ]

    operations = [
        migrations.AddField(
            model_name='eczstaff',
            name='subject',
            field=models.ForeignKey(blank=True, db_column='Subject_Code', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Examiner.subject', to_field='subjectCode'),
        ),
    ]
