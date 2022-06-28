# Generated by Django 4.0.5 on 2022-06-28 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20)),
                ('file_name', models.CharField(max_length=200)),
                ('docfile', models.FileField(upload_to='documents/')),
                ('last_access', models.DateTimeField(auto_now=True)),
                ('rows', models.IntegerField()),
                ('columns', models.IntegerField()),
            ],
        ),
    ]