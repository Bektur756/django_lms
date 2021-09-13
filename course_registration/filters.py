from django_filters import rest_framework as filters

from course_registration.models import Registration
from accounts.models import User


class RegistrationFilter(filters.FilterSet):
    total_sum_from = filters.NumberFilter(field_name='total_sum',
                                          lookup_expr='gte')
    total_sum_to = filters.NumberFilter(field_name='total_sum',
                                        lookup_expr='lte')
    student = filters.CharFilter(field_name=User),
    created_at = filters.DateFilter(field_name='created')
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Registration
        fields = ('status',)
