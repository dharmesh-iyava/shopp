# Generated by Django 3.0.3 on 2020-06-06 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('label', models.CharField(choices=[('S', 'Shirt'), ('P', 'Pant'), ('T', 'T-Shirt')], max_length=1)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
