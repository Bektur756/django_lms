from rest_framework import serializers

from .models import Registration, CourseRegistration


class CourseRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseRegistration
        exclude = ('id', 'registration')


class RegistrationSerializer(serializers.ModelSerializer):
    subjects = CourseRegistrationSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Registration
        exclude = ('courses')

    def create(self, validated_data):
        request = self.context.get('request')
        subjects = validated_data.pop('subjects')
        user = request.user
        registration = Registration.objects.create(user=user)
        total = 0
        for subject in subjects:
            total += subject['hotel'].credits * subject['quantity']
            CourseRegistration.objects.create(reservation=reservation,
                                     course=subject['course'],
                                     quantity=subject['quantity'])
        registration.total_sum = total
        registration.save()
        return registration