import datetime

from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from .models import SalesForce
from .permissions import MainSalesForcePermissionClass
from .serializers import SalesForceSerializer


class MainSalesForceViewSet(viewsets.ModelViewSet):
    serializer_class = SalesForceSerializer
    queryset = SalesForce.objects.all().order_by('-creation_timestamp')
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        MainSalesForcePermissionClass,
    ]

    def list(self, request: Request, *args, **kwargs):
        queryset = self.queryset.filter(is_done=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalesForceStatsViewSet(viewsets.ViewSet):
    serializer_class = SalesForceSerializer
    queryset = SalesForce.objects.all().order_by('-creation_timestamp')
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        MainSalesForcePermissionClass,
    ]

    def get_expired_tickets(self):
        unfinished_tickets = self.queryset.filter(is_done=False)
        current_datetime = datetime.datetime.now()
        return [
            ticket.salesforce_number for ticket in unfinished_tickets
            if current_datetime - ticket.creation_timestamp.replace(tzinfo=None)
            >= datetime.timedelta(days=7)
        ]

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
