# Generated by Django 5.1.7 on 2025-03-26 16:26

import django.core.validators
import django.db.models.deletion
import trips.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(help_text='Kod waluty (np. PLN, EUR, USD)', max_length=3, verbose_name='Kod waluty')),
            ],
            options={
                'verbose_name': 'Waluta',
                'verbose_name_plural': 'Waluty',
                'db_table': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nazwa', max_length=124, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Typ wydatku',
                'verbose_name_plural': 'Typy wydatków',
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nazwa', max_length=124, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Typ biletu',
                'verbose_name_plural': 'Typy biletów',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nazwa', max_length=50, verbose_name='Nazwa')),
                ('start_date', models.DateField(help_text='Data rozpoczęcia', verbose_name='Data rozpoczęcia')),
                ('end_date', models.DateField(help_text='Data zakończenia', verbose_name='Data zakończenia')),
                ('settings', models.JSONField(default=dict, help_text='Ustawienia', verbose_name='Ustawienia')),
                ('creator', models.ForeignKey(help_text='Właściciel', on_delete=django.db.models.deletion.CASCADE, related_name='trips_as_creator', to='users.userprofile', verbose_name='Właściciel')),
                ('members', models.ManyToManyField(blank=True, help_text='Profil', related_name='trips_as_member', to='users.userprofile', verbose_name='Profil')),
            ],
            options={
                'verbose_name': 'Wycieczka',
                'verbose_name_plural': 'Wycieczki',
                'db_table': 'trips',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(help_text='Bilet', upload_to='tickets/', verbose_name='Bilet')),
                ('valid_from', models.DateTimeField(blank=True, help_text='Ważny od', null=True, verbose_name='Ważny od')),
                ('profile', models.ForeignKey(help_text='Profil', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='users.userprofile', verbose_name='Profil')),
                ('type', models.ForeignKey(default=trips.models.get_default_ticket_type, help_text='Typ', on_delete=django.db.models.deletion.CASCADE, to='trips.tickettype', verbose_name='Typ')),
                ('trip', models.ForeignKey(help_text='Wycieczka', on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='trips.trip', verbose_name='Wycieczka')),
            ],
            options={
                'verbose_name': 'Bilet',
                'verbose_name_plural': 'Bilety',
                'db_table': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='Tytuł wydatku', max_length=255, verbose_name='Tytuł')),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text='Kwota wydatku', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Kwota wydatku')),
                ('date', models.DateField(help_text='Data wydatku', verbose_name='Data')),
                ('note', models.TextField(blank=True, help_text='Notatka dotycząca wydatku (opcjonalne)', verbose_name='Notatka')),
                ('currency', models.ForeignKey(default=trips.models.get_default_currency, help_text='Waluta wydatku', on_delete=django.db.models.deletion.PROTECT, to='trips.currency', verbose_name='Waluta')),
                ('user', models.ForeignKey(blank=True, help_text='Osoba, która poniosła wydatek', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='users.userprofile', verbose_name='Użytkownik')),
                ('category', models.ForeignKey(default=trips.models.get_default_expense_type, help_text='Kategoria wydatku', on_delete=django.db.models.deletion.CASCADE, to='trips.expensetype', verbose_name='Kategoria')),
                ('trip', models.ForeignKey(help_text='Powiązana podróż', on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='trips.trip', verbose_name='Podróż')),
            ],
            options={
                'verbose_name': 'Wydatek',
                'verbose_name_plural': 'Wydatki',
                'db_table': 'expenses',
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text='Kwota budżetu', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Kwota budżetu')),
                ('currency', models.CharField(help_text='Waluta (np. USD, PLN)', max_length=10, verbose_name='Waluta')),
                ('trip', models.OneToOneField(help_text='Powiązana wycieczka', on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='trips.trip', verbose_name='Wycieczka')),
            ],
            options={
                'verbose_name': 'Budżet',
                'verbose_name_plural': 'Budżety',
                'db_table': 'budgets',
            },
        ),
        migrations.CreateModel(
            name='TripAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(help_text='Token', max_length=24, verbose_name='Token')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_tokens', to='trips.trip')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
            options={
                'verbose_name': 'Token dostępu do wycieczki',
                'verbose_name_plural': 'Tokeny dostępu do wycieczek',
                'unique_together': {('trip', 'user_profile')},
            },
        ),
    ]
