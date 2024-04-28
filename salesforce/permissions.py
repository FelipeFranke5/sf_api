from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class MainSalesForcePermissionClass(permissions.BasePermission):

    def has_permission(self, request: Request, view: APIView):
        if request.method in SAFE_METHODS:
            return bool(
                request.user.has_perm('salesforce.view_salesforce')
            )

        match request.method:
            case 'POST':
                return bool(
                    request.user.has_perm('salesforce.add_salesforce')
                )
            case 'PUT' | 'PATCH':
                return bool(
                    request.user.has_perm('salesforce.change_salesforce')
                )
            case 'DELETE':
                return bool(
                    request.user.has_perm('salesforce.delete_salesforce')
                )
            case _:
                return False
