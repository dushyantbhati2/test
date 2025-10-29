from rest_framework.routers import DefaultRouter
from .views import VesselViewSet

router = DefaultRouter()
router.register(r'', VesselViewSet)

urlpatterns = router.urls
