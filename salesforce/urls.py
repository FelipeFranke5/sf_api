from rest_framework.routers import DefaultRouter

from .views import (MainSalesForceViewSet, SalesForceStatsViewSet)

# Set up the default ROUTER
router = DefaultRouter()

# Router for the SalesForce C.R.U.D via API
router.register(
    r'salesforce',
    MainSalesForceViewSet,
)

# Router for the SalesForce stats
router.register(
    r'salesforce-stats',
    SalesForceStatsViewSet,
    basename='salesforce-stats'
)

urlpatterns = router.urls
