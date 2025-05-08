import re

from django.core.validators import RegexValidator


phone_number_re = re.compile(r'^\+?(\d{1,3})?[-.\s]?(\(?\d{1,4}\)?)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
validate_phone_number = RegexValidator(phone_number_re, 'Enter a valid phone number consisting only numbers')

only_alphabetic_re = re.compile(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$')
validate_only_alphabetic = RegexValidator(only_alphabetic_re, 'Wprowadź poprawny alfabetystyczny ciąg znaków (bez cyfr i symboli).')
