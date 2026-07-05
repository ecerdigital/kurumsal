from django.contrib import admin
from .models import Gorev

@admin.register(Gorev)
class GorevAdmin(admin.ModelAdmin):
    # Admin panelinde hangi sütunlar yan yana görünsün?
    list_display = ('baslik', 'atanan_personel', 'tenant', 'baslangic_tarihi', 'durum')
    
    # Sağ tarafta hangi alanlara göre filtreleme kutusu açılansın?
    list_filter = ('durum', 'tenant', 'baslangic_tarihi')
    
    # Arama kutusunda hangi alanlarda arama yapılabilsin?
    search_fields = ('baslik', 'aciklama')