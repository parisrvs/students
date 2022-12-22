from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    StudentSerializer,
    UpdateStudentSerializer,
    ResultSerializer,
    UpdateResultSerializer
)
from .pagination import DefaultPagination
from .models import Student, Result


class StudentViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "post"]
    queryset = Student.objects.all().prefetch_related("results")
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "roll_number"]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateStudentSerializer
        return StudentSerializer


class ResultViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "post"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateResultSerializer
        return ResultSerializer

    def get_queryset(self):
        return Result.objects.filter(
            student_id=self.kwargs["student_pk"]
        ).select_related("student")

    def get_serializer_context(self):
        return {"student_id": self.kwargs["student_pk"]}
