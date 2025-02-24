# Generated by Django 5.1.5 on 2025-01-26 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FYQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FYQ',
                'verbose_name_plural': 'FYQ',
                'db_table': 'fyq',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nazwa', max_length=50, verbose_name='Nazwa')),
                ('budget', models.DecimalField(decimal_places=2, default=0, help_text='Budżet', max_digits=7, verbose_name='Budżet')),
                ('start_date', models.DateField(auto_now_add=True, help_text='Data rozpoczęcia', verbose_name='Data rozpoczęcia')),
                ('end_date', models.DateField(auto_now=True, help_text='Data zakończenia', verbose_name='Data zakończenia')),
                ('settings', models.JSONField(default=dict, help_text='Ustawienia', verbose_name='Ustawienia')),
                ('creator', models.ForeignKey(help_text='Właściciel', on_delete=django.db.models.deletion.CASCADE, related_name='trips_as_creator', to='users.userprofile', verbose_name='Właściciel')),
                ('members', models.ForeignKey(blank=True, help_text='Profil', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trips_as_member', to='users.userprofile', verbose_name='Profil')),
            ],
            options={
                'verbose_name': 'Wycieczka',
                'verbose_name_plural': 'Wycieczki',
                'db_table': 'trips',
            },
        ),
        migrations.CreateModel(
            name='TripActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nazwa', max_length=50, verbose_name='Nazwa')),
                ('budget', models.DecimalField(decimal_places=2, default=0, help_text='Budżet', max_digits=7, verbose_name='Budżet')),
                ('description', models.TextField(help_text='Opis', max_length=500, verbose_name='Opis')),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Data', verbose_name='Data')),
                ('trip', models.ForeignKey(help_text='Wycieczka', on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='trips.trip', verbose_name='Wycieczka')),
            ],
            options={
                'verbose_name': 'Aktywność na wycieczce',
                'verbose_name_plural': 'Aktywności na wycieczce',
                'db_table': 'trip_activities',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.FileField(help_text='Bilet', upload_to='tickets/', verbose_name='Bilet')),
                ('profile', models.ForeignKey(help_text='Profil', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='users.userprofile', verbose_name='Profil')),
                ('trip', models.ForeignKey(help_text='Wycieczka', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='trips.trip', verbose_name='Wycieczka')),
                ('activity', models.ForeignKey(help_text='Aktywność', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='trips.tripactivity', verbose_name='Aktywność')),
            ],
            options={
                'verbose_name': 'Bilet',
                'verbose_name_plural': 'Bilety',
                'db_table': 'tickets',
            },
        ),
    ]
