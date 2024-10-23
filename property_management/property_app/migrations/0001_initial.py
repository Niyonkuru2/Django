# Generated by Django 5.0.6 on 2024-10-19 16:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uu_id', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('property_type', models.CharField(choices=[('appartment', 'Appartment'), ('house', 'House'), ('commercial', 'Commercial')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('number_of_unit', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.PositiveIntegerField()),
                ('bedroom', models.PositiveIntegerField()),
                ('bathromm', models.PositiveIntegerField()),
                ('rent', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_Available', models.BooleanField(default=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='property_app.property')),
            ],
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rent_Ammount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_app.tenant')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_app.unit')),
            ],
        ),
    ]
