from django.contrib import admin
from .models import FinanceEntry

@admin.register(FinanceEntry)
class FinanceEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'entry_type', 'amount', 'description')
    list_filter = ('entry_type', 'date')
    search_fields = ('description',)