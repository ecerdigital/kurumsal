from rest_framework import serializers
from .models import Gorev
from personel.models import Employee

from rest_framework import serializers
from .models import Gorev

class GorevSerializer(serializers.ModelSerializer):
    # React'ın frontend'de atanan personelin adını 'atanan_personel_ad' olarak okuması için:
    atanan_personel_ad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Gorev
        fields = [
            'id', 'tenant', 'atanan_personel', 'atanan_personel_ad', 'atayan',
            'baslik', 'aciklama', 'baslangic_tarihi', 'bitis_tarihi', 
            'durum', 'tamamlanma_tarihi', 'olusturulma_tarihi', 'guncellenme_tarihi'
        ]
        # tenant ve atayan alanlarını frontend'den zorunlu beklememek için read_only yapıyoruz.
        # Bunları otomatik olarak views.py dolduracak.
        read_only_fields = ['id', 'tenant', 'atayan', 'durum', 'tamamlanma_tarihi']

    def get_atanan_personel_ad(self, obj):
        if obj.atanan_personel:
            return f"{obj.atanan_personel.first_name} {obj.atanan_personel.last_name}"
        return "Atanmamış"


class GorevTamamlaSerializer(serializers.ModelSerializer):
    """Görevi tamamlandı olarak işaretlerken kullanılan hafif serializer"""
    class Meta:
        model = Gorev
        fields = ['durum']

    def update(self, instance, validated_data):
        instance.durum = 'tamamlandi'
        instance.save()
        return instance