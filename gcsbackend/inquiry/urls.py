from rest_framework.routers import DefaultRouter
from .views import InquiryViewSet

router = DefaultRouter()
router.register(r'', InquiryViewSet, basename='inquiry')

urlpatterns = router.urls
 