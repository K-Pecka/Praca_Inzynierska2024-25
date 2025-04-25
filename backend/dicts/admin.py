from django.contrib import admin
from .models import SystemVariable

@admin.register(SystemVariable)
class SystemVariableAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "value_preview")
    list_filter = ("type",)
    search_fields = ("name",)

    def value_preview(self, obj):
        val = obj.value
        if isinstance(val, (dict, list)):
            import json
            val = json.dumps(val)
        return str(val)[:50] + "..." if len(str(val)) > 50 else str(val)

    value_preview.short_description = "Value"
