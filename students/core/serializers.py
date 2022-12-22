from rest_framework import serializers
from .models import Student, Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "id",
            "subject",
            "max_marks",
            "marks_obtained",
            "remark"
        ]

    def validate(self, attrs):
        subject = attrs.get("subject")
        max_marks = attrs.get("max_marks")
        marks_obtained = attrs.get("marks_obtained")
        student_id = self.context["student_id"]

        if not Student.objects.filter(id=student_id).exists():
            raise serializers.ValidationError(
                "Invalid Student ID",
                code="invalid"
            )

        if Result.objects.filter(
            student_id=student_id,
            subject=subject
        ).exists():
            raise serializers.ValidationError(
                "This subject already exists in the database.",
                code="duplicate"
            )

        if marks_obtained > max_marks:
            raise serializers.ValidationError(
                "Marks obtained cannot be greater than maximum marks.",
                code="matherror"
            )

        return attrs

    def create(self, validated_data):
        return Result.objects.create(
            student_id=self.context["student_id"],
            subject=validated_data["subject"],
            max_marks=validated_data["max_marks"],
            marks_obtained=validated_data["marks_obtained"],
            remark=validated_data["remark"]
        )


class UpdateResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "subject",
            "max_marks",
            "marks_obtained",
            "remark"
        ]

    def validate(self, attrs):
        instance = self.instance
        subject = attrs.get("subject")
        max_marks = attrs.get("max_marks")
        marks_obtained = attrs.get("marks_obtained")
        student_id = self.context["student_id"]

        if not Student.objects.filter(id=student_id).exists():
            raise serializers.ValidationError(
                "Invalid Student ID",
                code="invalid"
            )

        if instance.subject != subject and Result.objects.filter(
            student_id=student_id,
            subject=subject
        ).exists():
            raise serializers.ValidationError(
                "This subject already exists in the database.",
                code="duplicate"
            )

        if marks_obtained > max_marks:
            raise serializers.ValidationError(
                "Marks obtained cannot be greater than maximum marks.",
                code="matherror"
            )

        return attrs


class StudentSerializer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateField(source="dob")
    results = ResultSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "student_class",
            "roll_number",
            "dob",
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

        try:
            average = sum // count
        except ZeroDivisionError:
            return 0
        else:
            return average


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "name",
            "student_class",
            "roll_number",
            "dob",
            "gender",
            "mobile"
        ]
