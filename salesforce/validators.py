from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_salesforce_has_8_digits_only(value: str):
    value_length = len(value)

    if value_length != 8:
        raise ValidationError(
            message=_(
                f'expected 8 characters but received {value_length} instead'
            ),
            params={'value': value},
        )


def validate_establishment_code_has_10_digits_only(value: str):
    value_length = len(value)

    if value_length != 10:
        raise ValidationError(
            message=_(
                f'expected 10 characters but received {value_length} instead'
            ),
            params={'value': value},
        )


def validate_each_char_is_digit(value: str):
    for char in value:
        if not char.isdigit():
            raise ValidationError(
                message=_(
                    f'expected only numbers, got {value}. {char} is not \
allowed'
                ),
                params={'value': value},
            )
