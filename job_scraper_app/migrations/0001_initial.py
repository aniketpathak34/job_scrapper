# Generated by Django 4.2.4 on 2023-08-18 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('company_name', models.CharField(max_length=200)),
                ('company_location', models.CharField(max_length=100)),
                ('company_salary', models.CharField(max_length=200)),
            ],
        ),
    ]