"""
Tests for models.
"""

from django.test import TestCase
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError

from core.models import Student

from datetime import date
import string
import random


class ModelTest(TestCase):
    def test_create_student_model_successful(self):
        """Test to successfully create a student."""
        payload = {
            "name": "student",
            "student_class": "01",
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "9876543210"
        }

        student = Student.objects.create(**payload)

        self.assertEqual(student.name, payload["name"])
        self.assertEqual(student.student_class, payload["student_class"])
        self.assertEqual(student.roll_number, payload["roll_number"])
        self.assertEqual(student.dob, payload["dob"])
        self.assertEqual(student.gender, payload["gender"])
        self.assertEqual(student.mobile, payload["mobile"])

    def test_create_student_model_with_invalid_name(self):
        """
        Test to create a student with 40+ character name, returns DataError.
        """

        # Invalid value
        name = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=41
        ))

        payload = {
            "name": name,  # Invalid value
            "student_class": "01",
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "9876543210"
        }

        with self.assertRaises(DataError):
            Student.objects.create(**payload)

    def test_create_student_model_with_null_values(self):
        """
        Test to create a student with name = None, returns IntegrityError.
        """

        payload = {
            "name": None,  # Invalid value
            "student_class": "01",
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "1234567890"
        }

        with self.assertRaises(IntegrityError):
            Student.objects.create(**payload)

    def test_create_student_model_with_invalid_mobile_number(self):
        """Test to create student model with characters in a mobile number."""

        payload = {
            "name": "student",
            "student_class": "01",
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "12345fe67dw890"  # Invalid value
        }

        student = Student.objects.create(**payload)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_create_student_model_with_invalid_choice_field(self):
        """Test to create student model with invalid student_class value."""

        payload = {
            "name": "student",
            "student_class": "abcd",  # Invalid value
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "12345fe67dw890"
        }

        with self.assertRaises(DataError):
            Student.objects.create(**payload)
