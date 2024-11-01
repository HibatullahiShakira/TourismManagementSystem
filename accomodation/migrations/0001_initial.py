# Generated by Django 5.1.2 on 2024-10-25 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('availability', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=1000)),
                ('images', models.ImageField(blank=True, null=True, upload_to='', verbose_name='images/')),
                ('accommodation_type', models.CharField(choices=[('A', 'ACCOMMODATION'), ('S', 'HOME STAYS'), ('H', 'HOTELS')], default='HOTELS', max_length=10)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.tour')),
            ],
        ),
    ]