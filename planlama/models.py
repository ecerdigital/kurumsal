from django.db import models
from django.conf import settings
from core.models import Tenant  # Sizin projenizdeki Tenant modelinin yolu
from personel.models import Employee  # Sizin projenizdeki Employee modelinin yolu

class Gorev(models.Model):
    class Durum(models.TextChoices):
        BEKLIYOR = "bekliyor", "Bekliyor"
        TAMAMLANDI = "tamamlandi", "Tamamlandı"

    # --- ŞİRKET İZOLASYON ALANI ---
    # null=True ve blank=True ekledik. Böylece şirket eşleşmesi 
    # o an yapılamazsa bile veritabanı 500 hatası fırlatarak çökmeyecek.
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        related_name="gorevler",
        null=True,
        blank=True
    )

    # Görev kime atandı (Zorunlu alan - Her görevin bir sorumlusu olmalı)
    atanan_personel = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name="gorevler"
    )

    # Görevi kim atadı (Görevi oluşturan kişi personel olmasa bile User ID'si buraya yazılır)
    atayan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atadigi_gorevler",
    )

    # Görev Detayları
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField(blank=True)

    # Tarihler
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()

    # Durum Yönetimi
    durum = models.CharField(
        max_length=20, 
        choices=Durum.choices, 
        default=Durum.BEKLIYOR
    )
    tamamlanma_tarihi = models.DateTimeField(null=True, blank=True)

    # Audit (Zaman Damgaları)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["baslangic_tarihi"]
        indexes = [
            models.Index(fields=["tenant", "atanan_personel"]),
        ]

    def __str__(self):
        return f"{self.baslik} -> {self.atanan_personel}"

    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
        
    #     # --- AJAN LOGLARI (Terminalde durumu görmek için) ---
    #     print("\n--- GÖREV KAYDEDİLİYOR ---")
    #     print(f"1. Bu yeni bir görev mi?: {is_new}")
    #     if self.atanan_personel:
    #         print(f"2. Atanan Personel Bulundu: {self.atanan_personel.first_name}")
    #         print(f"3. Personelin E-postası var mı?: '{self.atanan_personel.email}'")
    #     else:
    #         print("2. ❌ UYARI: Atanan personel bilgisi BOŞ geld!")
    #     print("---------------------------\n")
    #     # ----------------------------------------------------

    #     super().save(*args, **kwargs)
        
    #     # Kodun çalışması için buradaki şartları kontrol ediyoruz
    #     if is_new and self.atanan_personel and self.atanan_personel.email:
    #         try:
    #             print("🔄 Mail gönderme işlemi başlatılıyor...")
    #             konu = f"🆕 Yeni Görev Atandı: {self.baslik}"
    #             mesaj = f"Merhaba {self.atanan_personel.first_name},\n\nSana yeni bir görev tanımlandı.\n\n📌 Başlık: {self.baslik}"
                
    #             send_mail(
    #                 subject=konu,
    #                 message=mesaj,
    #                 from_email=settings.DEFAULT_FROM_EMAIL,
    #                 recipient_list=[self.atanan_personel.email],
    #                 fail_silently=False,
    #             )
    #             print("✅ MAİL BAŞARIYLA GÖNDERİLDİ!")
    #         except Exception as e:
    #             print(f"❌ MAİL GÖNDERİLİRKEN HATA: {e}")
    #     else:
    #         print("⚠️ Şartlar sağlanmadığı için mail gönderme fonksiyonu TETİKLENMEDİ.")