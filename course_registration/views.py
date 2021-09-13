from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, permissions

from .filters import RegistrationFilter
from .models import Registration

from .serializers import RegistrationSerializer


class RegistrationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RegistrationFilter

    def get_queryset(self):
        user = self.request.user
        return Registration.objects.filter(user=user)