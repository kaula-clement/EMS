# Generated by Django 4.1.1 on 2022-11-30 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examiner', '0025_remove_eczstaff_paper_remove_eczstaff_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='eczstaff',
            name='center',
            field=models.CharField(blank=True, choices=[('LUSAKA', 'LUSAKA'), ('COPPERBELT', 'COPPERBELT'), ('MONZE', 'MONZE'), ('KAPIRI', 'KAPIRI'), ('LIVINGSTONE', 'LIVINGSTONE'), ('CHOMA', 'CHOMA'), ('MWANDI', 'MWANDI'), ('LUNTE', 'LUNTE'), ('MWENSE', 'MWENSE'), ('KASENENGWA', 'KASENENGWA'), ('CHISAMBA', 'CHISAMBA'), ('CHIBOMBO', 'CHIBOMBO')], max_length=50, null=True),
        ),
    ]
