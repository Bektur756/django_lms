from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    credits = models.IntegerField()
    image = models.ImageField(upload_to='images',
                              null=True,
                              blank=True)

    class Meta:
        ordering = ['course_name', 'credits']

    def __str__(self):
        return self.course_name


class CourseReview(models.Model):
    course_name = models.ForeignKey(Course,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    student = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')

    text = models.TextField()
    likes = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)