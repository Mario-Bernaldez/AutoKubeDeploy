import re
from django.core.exceptions import ValidationError


def validate_int_or_percent(value):
    if not re.match(r"^\d+%?$", value):
        raise ValidationError(
            "Must be an integer or a percentage (e.g., '1' or '25%')."
        )


def validate_ports(value):
    if value:
        try:
            port_list = [int(p) for p in value.split(",")]
        except ValueError:
            raise ValidationError("Only comma-separated numbers are allowed.")

        for port in port_list:
            if port < 1 or port > 65535:
                raise ValidationError(
                    f"Invalid port: {port}. Must be between 1 and 65535."
                )


def validate_absolute_path(value):
    if value and not value.startswith("/"):
        raise ValidationError("The path must be absolute (must start with '/').")


def validate_medium(value):
    if value and value != "Memory":
        raise ValidationError("The value must be 'Memory' or left empty.")


def validate_size_limit(value):
    if value:
        if not re.match(r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$", value):
            raise ValidationError("Invalid format. Valid examples: 500Mi, 1Gi, 1024Ki.")
