# Generated by Django 4.0.6 on 2022-08-27 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Examiner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=None)),
                ('name', models.CharField(default=None, max_length=50)),
            ],
        ),
    ]
