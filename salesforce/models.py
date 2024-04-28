import uuid

from django.db import models

from .validators import (validate_each_char_is_digit,
                         validate_establishment_code_has_10_digits_only,
                         validate_salesforce_has_4_digits_only)


class SalesForce(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    salesforce_number = models.CharField(
        verbose_name='SalesForce Number',
        help_text='Insert the SF number (6 digits)',
        validators=[
            validate_salesforce_has_4_digits_only,
            validate_each_char_is_digit,
        ],
        max_length=6,
        unique=True,
    )
    establishment_code = models.CharField(
        verbose_name='N. EC',
        help_text='Insert the EC number (10 digits)',
        validators=[
            validate_establishment_code_has_10_digits_only,
            validate_each_char_is_digit,
        ],
        max_length=10,
        default='0000000000',
    )
    description = models.CharField(
        verbose_name='Description',
        help_text='Insert a short description (max 255 characters)',
        max_length=255,
        default='N/A',
    )
    incident = models.CharField(
        verbose_name='Incident Protocol',
        help_text='Starts with INC or RITM',
        blank=True,
        null=True,
        max_length=25,
    )
    is_done = models.BooleanField(
        verbose_name='Ticket Done',
        help_text='Mark as done when necessary',
        default=False
    )
    notes = models.TextField(
        verbose_name='PS',
        help_text='Insert additional notes if necessary',
        default='N/A',
    )
    creation_timestamp = models.DateTimeField(
        verbose_name='Date/Time of Creation',
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.description
