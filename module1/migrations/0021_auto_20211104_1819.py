# Generated by Django 3.2 on 2021-11-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0020_auto_20211103_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdata',
            name='patientDate',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='patientdata',
            name='patientName',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='userdocdata',
            name='userName',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='patientdata',
            name='age',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='patientdata',
            name='gender',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='patientdata',
            name='userDID',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='updatedweights',
            name='age',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='updatedweights',
            name='gender',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='updatedweights',
            name='userDID',
            field=models.CharField(max_length=100),
        ),
    ]
