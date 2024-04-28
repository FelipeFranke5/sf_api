from rest_framework.routers import DefaultRouter

from .views import (MainSalesForceViewSet, SalesForceExcelViewSet,
                    SalesForceStatsViewSet)

# Set up the default ROUTER
router = DefaultRouter()

# Router for the SalesForce C.R.U.D via API
router.register(
    r'salesforce',
    MainSalesForceViewSet,
)

# Router for the SalesForce-to-Excel export
router.register(
    r'salesforce-xl',
    SalesForceExcelViewSet,
    basename='salesforce-xl',
)

# Router for the SalesForce stats
router.register(
    r'salesforce-stats',
    SalesForceStatsViewSet,
    basename='salesforce-stats'
)

urlpatterns = router.urls
