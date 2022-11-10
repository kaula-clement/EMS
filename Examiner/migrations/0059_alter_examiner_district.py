# Generated by Django 4.1.1 on 2022-11-10 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0058_examiner_to_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examiner',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Examiner.station'),
        ),
    ]