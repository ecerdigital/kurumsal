from django.db.models import Sum
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .serializers import FinanceEntrySerializer
from .models import FinanceEntry

class FinanceEntryViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'entry_type']
    queryset = FinanceEntry.objects.none()

    def get_queryset(self):
        if hasattr(self.request.user, 'tenant') and self.request.user.tenant:
            return FinanceEntry.objects.filter(tenant=self.request.user.tenant)
        return FinanceEntry.objects.none()

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        target_date = request.query_params.get('date')
        if not target_date:
            return Response({"error": "Tarih gerekli"}, status=status.HTTP_400_BAD_REQUEST)
        
        summary = FinanceEntry.objects.filter(
            tenant=self.request.user.tenant, 
            date=target_date
        ).values('entry_type').annotate(total=Sum('amount'))
        
        return Response(summary)