from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet,AddressViewSet,ContactViewSet

router = DefaultRouter()
router.register(r'address',AddressViewSet , basename='address')
router.register(r'contact',ContactViewSet, basename='contact')
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = router.urls