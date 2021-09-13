from rest_framework import serializers
from .models import Course, CourseReview


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'credits')


class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'description', 'credits', 'image', 'reviews')


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_credits(self, price):
        if price < 0:
            raise serializers.ValidationError('Количество кредитов не может быть отрицательным')
        return price


class ReviewSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CourseReview
        fields = ('id', 'student', 'course_name', 'text', 'rating', 'likes', 'created_at')

    def validate_course(self, hotel):
        request = self.context.get('request')
        user = request.user
        if self.Meta.model.objects.filter(course=Course, student=user).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв вчера')
        return hotel

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг может быть от одного до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)