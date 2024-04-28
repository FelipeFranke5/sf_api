import datetime

from rest_framework import serializers

from .models import SalesForce


class SalesForceSerializer(serializers.ModelSerializer):
    expiration_date = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()

    class Meta:
        model = SalesForce
        fields = [
            'id',
            'creation_timestamp',
            'expiration_date',
            'priority',
            'salesforce_number',
            'incident',
            'establishment_code',
            'is_done',
            'description',
            'notes',
        ]

    def get_expiration_date(self, obj: SalesForce):
        creation_timestamp = obj.creation_timestamp
        expiration_date = creation_timestamp + datetime.timedelta(days=7)
        expiration_date = expiration_date.replace(tzinfo=None)
        expiration_date = expiration_date.strptime(
            expiration_date.strftime('%d/%m/%yT%H:%M:%S'),
            '%d/%m/%yT%H:%M:%S',
        )
        return expiration_date

    def get_priority(self, obj: SalesForce):
        creation_timestamp = obj.creation_timestamp
        creation_timestamp = creation_timestamp.replace(tzinfo=None)
        expiration_date = creation_timestamp + datetime.timedelta(days=7)
        current_date = datetime.datetime.now()

        if current_date >= expiration_date:
            return 'URGENT'

        time_difference = expiration_date - current_date
        if time_difference <= datetime.timedelta(days=2):
            return 'High'

        if time_difference <= datetime.timedelta(days=5):
            return 'Medium'

        return 'Low'
