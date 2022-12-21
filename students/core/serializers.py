from rest_framework import serializers
from .models import Student, Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "subject",
            "max_marks",
            "marks_obtained",
            "remark"
        ]


class StudentSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(source="dob")
    results = ResultSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "student_class",
            "roll_number",
            "date_of_birth",
            "gender",
            "mobile",
            "subjects_count",
            "results",
            "average"
        ]

    subjects_count = serializers.SerializerMethodField(
        method_name="get_subjects_count",
        read_only=True
    )
    average = serializers.SerializerMethodField(
        method_name="get_average",
        read_only=True
    )

    def get_subjects_count(self, student: Student):
        return student.results.all().count()

    def get_average(self, student: Student):
        count = 0
        sum = 0
        for result in student.results.all():
            sum += result.marks_obtained
            count += 1

        return sum // count
