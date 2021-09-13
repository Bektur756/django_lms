from django.db import models
from courses.models import Course
from accounts.models import User as Student
from django.contrib.auth import get_user_model


User = get_user_model()

STATUS_CHOICES = (
    ('required', 'обязательный'),
    ('prerequisite', 'требуется пререквизиты'),
    ('free', 'свободный')
)


class Registration(models.Model):
    total_credits = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             related_name='registrations')
    status = models.CharField(max_length=20,
                              choices = STATUS_CHOICES,
                              default='free')
    courses = models.ManyToManyField(Course,
                                      through='CourseRegistration')

    @property
    def total(self):
        subjects = self.subjects.values('registration', 'quantity')
        total = 0
        for subject in subjects:
            total += subject['registration'] * subject['quantity']
        return total

    def __str__(self):
        return f'Курс зарегестрирован {self.id} от {self.created_at.strftime("%d-%m-%Y %H:%M")}'

    class Meta:
        db_table = 'registration'
        ordering = ['-created_at']


class CourseRegistration(models.Model):
    registration = models.ForeignKey(Registration,
                              on_delete=models.RESTRICT,
                              related_name='subjects')
    course = models.ForeignKey(Course,
                                on_delete=models.RESTRICT,
                                related_name='register_subjects')

    student = models.ForeignKey(Student,
                                on_delete=models.RESTRICT,
                                related_name='registered_user')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'register_subjects'
    #class Meta для того, чтобы задать параметры общие, не касающиеся какого-то конкретного поля