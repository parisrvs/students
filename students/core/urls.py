from django.urls import path, include
from rest_framework_nested import routers
from .views import StudentViewSet, ResultViewSet

router = routers.DefaultRouter()
router.register("students", StudentViewSet)

students_router = routers.NestedDefaultRouter(
    router,
    "students",
    lookup="student"
)
students_router.register(
    "results",
    ResultViewSet,
    basename="student-results"
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(students_router.urls)),
]
