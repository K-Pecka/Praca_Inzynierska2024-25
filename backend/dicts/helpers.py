from django.utils.safestring import mark_safe

def get_admin_change_link(obj):
    """
    Helper function to return an admin change link for a given model instance.
    """
    if obj:
        return mark_safe(
            f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/change/">{obj}</a>'
        )
    return "No profile"
