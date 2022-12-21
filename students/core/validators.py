from django.core.exceptions import ValidationError


def validate_number(value: str):
    if not value.isdigit():
        raise ValidationError(
            "Enter valid digits."
        )
    return value
