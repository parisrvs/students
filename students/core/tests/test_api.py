"""
Test project apis
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from datetime import date
from core.models import Student, Result


def create_student():
    payload = {
        "name": "Test Name",
        "student_class": "04",
        "roll_number": "9876784445",
        "dob": date.today().isoformat(),
        "gender": "M",
        "mobile": "9876543210"
    }
    return Student.objects.create(**payload)


class StudentAPITests(TestCase):
    """Test the features of student API."""

    def setUp(self):
        self.client = APIClient()

    def test_successfully_create_student(self):
        """Test to successfully create a student."""

        payload = {
            "name": "Test Name",
            "student_class": "04",
            "roll_number": "9876784445",
            "dob": date.today().isoformat(),
            "gender": "M",
            "mobile": "9876543210"
        }

        res = self.client.post(
            reverse("student-list"),
            payload,
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_student_with_invalid_choice(self):
        """Test create student with invalid student_class"""

        payload = {
            "name": "Test Name",
            "student_class": "111",  # invalid choice
            "roll_number": "9876784445",
            "dob": date.today().isoformat(),
            "gender": "M",
            "mobile": "9876543210"
        }

        res = self.client.post(
            reverse("student-list"),
            payload,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_with_invalid_data(self):
        """Test create student with invalid roll_number"""

        payload = {
            "name": "Test Name",
            "student_class": "04",
            "roll_number": "98767nndw84445",  # invalid choice
            "dob": date.today().isoformat(),
            "gender": "M",
            "mobile": "9876543210"
        }

        res = self.client.post(
            reverse("student-list"),
            payload,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class StudentDetailAPITests(TestCase):
    def setUp(self):
        """setup a dummy student and api client"""

        self.student = create_student()
        self.client = APIClient()

    def test_get_student_detail(self):
        """Test GET request to /api/students/<int:student_pk>/ endpoint"""

        self.student = create_student()
        res = self.client.get(
            reverse("student-detail", args=[self.student.id]),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.student.id)

    def test_patch_student_detail(self):
        """Test PATCH request to /api/students/<int:student_pk>/ endpoint"""

        res = self.client.patch(
            reverse("student-detail", args=[self.student.id]),
            {"name": "Updated Name"}
        )

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Updated Name")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_student_detail_invalid_data(self):
        """
        Test PATCH request to /api/students/<int:student_pk>/ endpoint
        with invalid roll_number
        """

        res = self.client.patch(
            reverse("student-detail", args=[self.student.id]),
            {"roll_number": "abcd"}  # Invalid value
        )

        roll_number = self.student.roll_number
        self.student.refresh_from_db()
        self.assertEqual(self.student.roll_number, roll_number)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ResultAPITest(TestCase):

    """setup a dummy student, result of two subjects, and api client"""

    def setUp(self):
        self.student = create_student()

        self.result_phy = Result.objects.create(
            student=self.student,
            subject="PHY",
            max_marks=100,
            marks_obtained=90,
            remark="test remark 1"
        )

        self.result_che = Result.objects.create(
            student=self.student,
            subject="CHE",
            max_marks=100,
            marks_obtained=62,
            remark="test remark 2"
        )
        self.client = APIClient()

    def test_get_request_to_result_endpoint(self):
        res = self.client.get(reverse(
            "student-results-list",
            kwargs={"student_pk": self.student.id}
        ))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.result_che.id)

    def test_post_request_to_result_endpoint_with_valid_data(self):
        """returns 201 created"""
        res = self.client.post(
            reverse(
                "student-results-list",
                kwargs={"student_pk": self.student.id}
            ),
            {
                "subject": "BIO",
                "max_marks": 100,
                "marks_obtained": 87,
                "remark": "some test remark"
            }
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_request_to_result_endpoint_with_invalid_subject_choice(self):
        """returns 400"""
        res = self.client.post(
            reverse(
                "student-results-list",
                kwargs={"student_pk": self.student.id}
            ),
            {
                "subject": "AWS",  # invalid data
                "max_marks": 100,
                "marks_obtained": 87,
                "remark": "some test remark"
            }
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_duplicate_subject_choice(self):
        """test post request to result endpoint, returns 400"""
        res = self.client.post(
            reverse(
                "student-results-list",
                kwargs={"student_pk": self.student.id}
            ),
            {
                "subject": self.result_che.subject,  # duplicate subject
                "max_marks": 100,
                "marks_obtained": 87,
                "remark": "some test remark"
            }
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_request_to_result_endpoint_with_valid_data(self):
        res = self.client.patch(
            reverse(
                "student-results-detail",
                kwargs={
                    "student_pk": self.student.id,
                    "pk": self.result_che.id
                }
            ),
            {
                "subject": "BIO",
                "max_marks": 100,
                "marks_obtained": 87,
                "remark": "some test remark"
            }
        )

        self.result_che.refresh_from_db()
        self.assertEqual(self.result_che.subject, "BIO")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_request_to_result_endpoint_with_invalid_data(self):
        """
        Test patch request with duplicate data
        """
        res = self.client.patch(
            reverse(
                "student-results-detail",
                kwargs={
                    "student_pk": self.student.id,
                    "pk": self.result_che.id
                }
            ),
            {
                "subject": "PHY",
                "max_marks": 100,
                "marks_obtained": 87,
                "remark": "some test remark"
            }
        )

        subject = self.result_che.subject
        self.result_che.refresh_from_db()
        self.assertEqual(self.result_che.subject, subject)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
