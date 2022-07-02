# Generated by Django 3.2.7 on 2022-07-02 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('client', models.IntegerField()),
                ('currency', models.CharField(max_length=20)),
                ('type_of_account', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
