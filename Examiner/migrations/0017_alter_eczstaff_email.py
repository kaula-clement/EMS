# Generated by Django 4.1.1 on 2022-11-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0016_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eczstaff',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
