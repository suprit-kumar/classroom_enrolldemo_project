# Generated by Django 2.2.2 on 2021-04-03 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom_app', '0002_auto_20210318_0017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
    ]