# users/templatetags/user_extras.copy()

from django import template

register = template.Library()


@register.filter
def display_full_name(user) -> str:
    first = (getattr(user, "first_name", "") or "").strip()
    last = (getattr(user, "last_name", "") or "").strip()

    if first or last:
        return f"{first} {last}".strip()

    username = (getattr(user, "username", "") or "").strip()
    if not username:
        return "-"

    return username.replace("-", " ").replace("_", " ").title()
