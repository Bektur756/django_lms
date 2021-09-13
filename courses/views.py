from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from .models import Course, CourseReview
from .permissions import IsStaffOrIsAdmin, IsStudent
from .serializers import (CourseSerializer, CourseDetailsSerializer,
                          CreateCourseSerializer, ReviewSerializer)


@api_view(['GET'])
def hotel_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


class CourseFilter(filters.FilterSet):
    credits_from = filters.NumberFilter('credits', 'gte')
    credits_to = filters.NumberFilter('credits', 'lte')

    class Meta:
        model = Course
        fields = ('credits_from', 'credits_to')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['course_name', 'description']
    ordering_fields = ['course_name', 'credits']

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseSerializer
        elif self.action == 'retrieve':
            return CourseDetailsSerializer
        return CreateCourseSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsStaffOrIsAdmin()]
        return []


    @action(['GET'], detail=True)
    def reviews(self, request, pl=None):
        hotel = self.get_object()
        reviews = hotel.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)


# Создает только залогиненный пользователь
# Редактировать или удалять может либо админ, либо автор

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = CourseReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsStudent()]
        return []
