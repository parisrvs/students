"""
Test for django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from core.models import Student

from datetime import date


class AdminSiteTests(TestCase):
    """test for django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
            username="admin"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            username="testuser"
        )

        payload = {
            "name": "student",
            "student_class": "01",
            "roll_number": "1234567876543",
            "dob": date.today().isoformat(),
            "gender": 'M',
            "mobile": "9876543210"
        }
        self.student = Student.objects.create(**payload)

    def test_users_list(self):
        """test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that edit user page works correctly."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """Test the create user page works."""

        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_students_list(self):
        """test that students are listed on page."""
        url = reverse("admin:core_student_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.student.name)
        self.assertContains(res, self.student.roll_number)
        self.assertContains(res, self.student.gender)
        self.assertContains(res, self.student.mobile)

    def test_edit_student_page(self):
        """Test that edit student page works correctly."""
        url = reverse("admin:core_student_change", args=[self.student.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_student_create_page(self):
        """Test the create student page works."""

        url = reverse("admin:core_student_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
