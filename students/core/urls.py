from django.urls import path, include
from rest_framework_nested import routers
from .views import StudentViewSet

router = routers.DefaultRouter()
router.register("students", StudentViewSet)


urlpatterns = [
    path('', include(router.urls))
]
