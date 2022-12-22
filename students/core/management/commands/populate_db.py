"""
Popolate database with dummy data.
"""

from django.core.management.base import BaseCommand
from core.models import Student, Result
import random
import string
from datetime import date, timedelta


def get_remark():
    """generate dummy remark."""
    sentences = ''
    for _ in range(random.randint(2, 5)):
        words = ''
        for _ in range(random.randint(4, 15)):
            words = words + \
                ''.join(random.choices(string.ascii_lowercase,
                        k=random.randint(2, 8))) + ' '

        words = words.strip() + '. '
        sentences += words.capitalize()
    return sentences.strip()


def get_digits(n):
    """generate dummy digits for roll number and mobile number."""
    digits = ''.join(random.choices(string.digits, k=n))
    return digits


def get_name():
    """generate dummy name."""
    first_name = ''.join(random.choices(
        string.ascii_lowercase,
        k=random.randint(4, 7)
    ))

    last_name = ''.join(random.choices(
        string.ascii_lowercase,
        k=random.randint(4, 7)
    ))
    name = f"{first_name.strip().title()} {last_name.strip().title()}"

    return name


CLASS_CHOICES = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
]


GENDER_CHOICES = [
    'M',
    'F',
    'O',
    'N',
]


SUBJECT_CHOICES = [
    "PHY",
    "CHE",
    "BIO",
    "EG1",
    "EG2",
    "MAT",
    "HIS",
    "GEO",
    "CMP",
]


class Command(BaseCommand):
    """Django command to populate database with dummy data"""

    def handle(self, *args, **options):
        """Entrypoint for command"""

        """Create dummy students"""
        for _ in range(100):
            Student.objects.create(
                name=get_name(),
                student_class=random.choice(CLASS_CHOICES),
                roll_number=get_digits(10),
                dob=(
                    date.today() - timedelta(
                        days=random.randint(365, 3650)
                    )
                ).isoformat(),
                gender=random.choice(GENDER_CHOICES),
                mobile=get_digits(10)
            )

        """Create dummy results"""
        for student in Student.objects.all():
            subjects = []
            for _ in range(random.randint(5, 9)):
                while True:
                    subject = random.choice(SUBJECT_CHOICES)
                    if subject not in subjects:
                        subjects.append(subject)
                        break

                Result.objects.create(
                    student=student,
                    subject=subject,
                    max_marks=100,
                    marks_obtained=random.randint(0, 100),
                    remark=get_remark()
                )
