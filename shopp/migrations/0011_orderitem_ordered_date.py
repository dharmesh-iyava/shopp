# Generated by Django 3.0.3 on 2020-06-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopp', '0010_remove_orderitem_ordered_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]