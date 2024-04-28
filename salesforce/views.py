import datetime

from django.utils.translation import gettext as _
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from . import excel_styling
from .models import SalesForce
from .permissions import MainSalesForcePermissionClass
from .serializers import SalesForceSerializer


class MainSalesForceViewSet(viewsets.ModelViewSet):
    serializer_class = SalesForceSerializer
    queryset = SalesForce.objects.all().order_by('-creation_timestamp')
    permission_classes = [
        IsAuthenticatedOrReadOnly, MainSalesForcePermissionClass
    ]


class SalesForceExcelViewSet(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SalesForceSerializer
    queryset = SalesForce.objects.filter(is_done=False).order_by(
        '-creation_timestamp'
    )
    renderer_classes = [XLSXRenderer]
    filename = f'SF - {datetime.datetime.now()}.xlsx'
    column_header = excel_styling.get_column_header()
    body = excel_styling.get_body()
    xlsx_ignore_headers = excel_styling.get_xlsx_ignore_headers()
    xlsx_boolean_labels = {True: _('true'), False: _('false')}


class SalesForceStatsViewSet(viewsets.ViewSet):
    serializer_class = SalesForceSerializer
    queryset = SalesForce.objects.all().order_by('-creation_timestamp')

    def get_expired_tickets(self):
        unfinished_tickets = self.queryset.filter(is_done=False)
        current_datetime = datetime.datetime.now()
        expired_tickets: list[str] = []

        for ticket in unfinished_tickets:
            days_7 = datetime.timedelta(days=7)
            creation_datetime = ticket.creation_timestamp.replace(tzinfo=None)

            if current_datetime - creation_datetime >= days_7:
                expired_tickets.append(ticket.salesforce_number)

        return expired_tickets

    def list(self, request: Request):
        total_tickets = self.queryset.count()
        finished_tickets = self.queryset.filter(is_done=True).count()
        expired_tickets = self.get_expired_tickets()
        last_ticket = self.queryset.last()
        last_ticket_num = last_ticket.salesforce_number if last_ticket else None
        return Response(
            data={
                'total_tickets_count': total_tickets,
                'finished_tickets_count': finished_tickets,
                'expired_tickets': expired_tickets,
                'last_ticket': last_ticket_num,
            },
            status=status.HTTP_200_OK,
        )
