from rest_framework import routers
from .views import BoardViewSet

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)
urlpatterns = router.urls
