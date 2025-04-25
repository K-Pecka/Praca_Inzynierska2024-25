import json
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VariableType(models.TextChoices):
    INT = 'int', 'Integer'
    FLOAT = 'float', 'Float'
    STR = 'str', 'String'
    BOOL = 'bool', 'Boolean'
    JSON = 'json', 'JSON'


class SystemVariable(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=VariableType.choices)
    int_value = models.IntegerField(null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)
    str_value = models.CharField(max_length=255, null=True, blank=True)
    bool_value = models.BooleanField(default=False)
    json_value = models.JSONField(null=True, blank=True)

    @property
    def value(self):
        """Zwraca wartość zmiennej na podstawie jej typu."""
        if self.type == 'int':
            return self.int_value
        elif self.type == 'float':
            return self.float_value
        elif self.type == 'str':
            return self.str_value
        elif self.type == 'bool':
            return self.bool_value
        elif self.type == 'json':
            return self.json_value

    @value.setter
    def value(self, val):
        self.int_value = self.float_value = self.str_value = self.json_value = None
        if self.type == 'int':
            self.int_value = int(val)
        elif self.type == 'float':
            self.float_value = float(val)
        elif self.type == 'str':
            self.str_value = str(val)
        elif self.type == 'bool':
            self.bool_value = bool(val)
        elif self.type == 'json':
            if isinstance(val, str):
                try:
                    self.json_value = json.loads(val)
                except json.JSONDecodeError:
                    raise ValidationError("Invalid JSON string.")
            else:
                self.json_value = val

    def get_absolute_url(self):
        """Zwraca URL do szczegółów zmiennej."""
        return reverse("system-variable-detail", kwargs={"pk": self.pk})

    def as_dict(self):
        """Zwraca słownik reprezentujący zmienną."""
        return {
            "name": self.name,
            "type": self.type,
            "value": self.value
        }

    def clean(self):
        """Walidacja, aby tylko jedno pole wartości było ustawione na podstawie typu."""
        values = {
            'int': self.int_value,
            'float': self.float_value,
            'str': self.str_value,
            'bool': self.bool_value,
            'json': self.json_value,
        }

        non_nulls = [v for v in values.values() if v is not None]
        if len(non_nulls) > 2 and not self.type == 'bool' or len(non_nulls) == 1 and self.type == 'bool':
            raise ValidationError("Tylko jedna wartość powinna być ustawiona.")

        if values[self.type] is None:
            raise ValidationError(f"Pole {self.type}_value musi być ustawione.")

    def save(self, *args, **kwargs):
        """Zapisuje obiekt po walidacji."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Zwraca reprezentację zmiennej w formacie tekstowym."""
        val = self.value
        if isinstance(val, (dict, list)):
            val = json.dumps(val)[:30] + "..." if len(json.dumps(val)) > 30 else json.dumps(val)
        return f"{self.name} ({self.type}) = {val}"

    class Meta:
        verbose_name = "System Variable"
        verbose_name_plural = "System Variables"
