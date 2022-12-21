from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all().prefetch_related("results")
