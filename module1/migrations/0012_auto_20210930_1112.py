# Generated by Django 3.2 on 2021-09-30 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0011_auto_20210927_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='updatedWeights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.CharField(max_length=100)),
                ('rubricRemedies', models.CharField(max_length=200)),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='patientdata',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
