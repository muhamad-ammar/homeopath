# Generated by Django 3.1.4 on 2022-05-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0025_updatedweights_weighttemp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatedweights',
            name='weightTemp',
            field=models.IntegerField(),
        ),
    ]
