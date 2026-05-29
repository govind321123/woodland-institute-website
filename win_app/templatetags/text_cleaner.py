from django import template

register = template.Library()

@register.filter
def clean_text(value):
    if not value:
        return value

    replacements = {
        "ΓÇÖ": "'",
        "â€™": "'",
        "â€“": "-",
        "â€œ": '"',
        "â€�": '"',
    }

    for bad, good in replacements.items():
        value = value.replace(bad, good)

    return value