# Generated by Django 4.1.2 on 2022-10-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=100)),
                ('beschrijving', models.CharField(max_length=250)),
                ('afbeelding', models.ImageField(upload_to='film/afbeeldingen/')),
                ('url', models.URLField(blank=True)),
            ],
        ),
    ]
