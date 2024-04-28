import json
from datetime import datetime
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from salesforce.models import SalesForce
from salesforce.serializers import SalesForceSerializer


class Command(BaseCommand):
    help = 'Send Email notification with pending tickets everyday at 6am'

    def handle(
        self,
        *args: Any,
        **options: dict[str, Any],
    ):
        current_time = datetime.now()
        self.stdout.write(
            msg='--NOTIFICATION SENDER LOG: TRIGGERED'
        )
        self.stdout.write(
            msg=f'--NOTIFICATION SENDER LOG: CURRENT HOUR: {current_time.hour}'
        )

        if current_time.hour == 6:
            self.stdout.write(
                msg='--NOTIFICATION SENDER LOG: ATTEMPTING TO SEND EMAIL'
            )
            notification_result = self.send_notification()

            if notification_result > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        '--NOTIFICATION SENDER LOG: EMAIL SENT SUCCESSFULLY'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        '--NOTIFICATION SENDER LOG: FAILED TO SEND EMAIL'
                    )
                )
        else:
            self.stdout.write(
                msg='--NOTIFICATION SENDER LOG: CANNOT SEND EMAIL RIGHT NOW'
            )

    def send_notification(self):
        host = settings.EMAIL_HOST_USER
        secure_email_address1 = settings.EMAIL_SECURE_ADD1
        date = f'{datetime.now().day}/{datetime.now().month}'
        subject = f'SalesForce Admin Report - {date}'
        recipient_list = [
            'frankefelipee@gmail.com',
            secure_email_address1,
        ]
        queryset_json = self.get_salesforce_pending_ticket()

        try:
            result = send_mail(
                subject=subject,
                message=queryset_json,
                from_email=host,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception:
            return 0
        return result

    def get_salesforce_pending_ticket(self):
        queryset = SalesForce.objects.all()
        queryset = queryset.order_by('-creation_timestamp')
        queryset = queryset.filter(is_done=False)
        serializer = SalesForceSerializer(queryset, many=True)
        json_object = json.dumps(serializer.data, indent=4, default=str)
        return json_object
