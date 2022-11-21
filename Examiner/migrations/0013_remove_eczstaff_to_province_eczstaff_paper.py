# Generated by Django 4.1.1 on 2022-11-18 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0012_markingvenue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eczstaff',
            name='to_province',
        ),
        migrations.AddField(
            model_name='eczstaff',
            name='paper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Examiner.paper'),
        ),
    ]