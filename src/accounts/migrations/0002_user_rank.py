# Generated by Django 4.2.6 on 2023-10-09 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.IntegerField(choices=[(0, 'Kozak'), (1, 'Otaman'), (2, 'Sotnyk'), (3, 'Polkovnyk'), (4, 'Koshovy'), (5, 'Hetman')], default=0, verbose_name='User rank'),
        ),
    ]