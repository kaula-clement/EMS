# Generated by Django 4.1.1 on 2022-11-09 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0053_session_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('district', models.ForeignKey(blank=True, db_column='district_code', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Examiner.district', to_field='code')),
            ],
        ),
    ]