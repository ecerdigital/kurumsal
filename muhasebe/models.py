from django.db import models
from django.utils import timezone
# 'Tenants' modelinin nerede olduğunu import etmelisin, örneğin:
from core.models import Tenant

class FinanceEntry(models.Model):
    TYPE_CHOICES = [
        ('alacak', 'Alacak'),
        ('borc', 'Borc'),
    ]

    # Tenant bağlantısını ekliyoruz
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name="Şirket")
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    entry_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="İşlem Tipi")
    description = models.TextField(verbose_name="Açıklama")
    date = models.DateField(default=timezone.now, verbose_name="İşlem Tarihi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} | {self.date} - {self.entry_type} - {self.amount}"

    class Meta:
        ordering = ['-date', '-created_at']