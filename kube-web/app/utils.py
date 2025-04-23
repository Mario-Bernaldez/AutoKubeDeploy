import re
from django.core.exceptions import ValidationError


def validate_int_or_percent(value):
    if not re.match(r"^\d+%?$", value):
        raise ValidationError(
            "Debe ser un número entero o un porcentaje (por ejemplo, '1' o '25%')."
        )


def validate_ports(value):
    if value:
        try:
            port_list = [int(p) for p in value.split(",")]
        except ValueError:
            raise ValidationError("Solo se permiten números separados por comas.")

        for port in port_list:
            if port < 1 or port > 65535:
                raise ValidationError(
                    f"Puerto inválido: {port}. Debe estar entre 1 y 65535."
                )


def validate_absolute_path(value):
    if value and not value.startswith("/"):
        raise ValidationError("La ruta debe ser absoluta (debe comenzar con '/').")


def validate_medium(value):
    if value and value != "Memory":
        raise ValidationError("El valor debe ser 'Memory' o estar vacío.")


def validate_size_limit(value):
    if value:
        if not re.match(r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$", value):
            raise ValidationError(
                "Formato inválido. Ejemplo válido: 500Mi, 1Gi, 1024Ki."
            )
