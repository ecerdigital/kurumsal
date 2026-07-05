from rest_framework import viewsets, permissions
from .models import Gorev
from .serializers import GorevSerializer
from personel.models import Employee

class GorevViewSet(viewsets.ModelViewSet):
    serializer_class = GorevSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Eğer giriş yapan kişi admin/superuser ise tüm görevleri görebilsin (Yönetim kolaylığı için)
        if user.is_superuser:
            return Gorev.objects.all()
            
        # Normal personel ise: Önce bu user'ın Employee kaydını buluyoruz.
        # İlk aldığımız hatayı hatırlayalım; Employee modelinde 'user' yoktu ama 'email' veya 'first_name' vardı.
        # User modeli ile Employee modelini 'email' üzerinden eşleştirelim (En güvenli yol):
        try:
            employee = Employee.objects.get(email=user.email)
            # Sadece bu personele atanmış görevleri filtrele
            return Gorev.objects.filter(atanan_personel=employee)
        except Employee.DoesNotExist:
            # Eğer bu kullanıcıya ait bir personel kartı bulunamadıysa hiçbir görev gösterme
            return Gorev.objects.none()

    def perform_create(self, serializer):
        # Önce görevi veritabanına kaydet ve oluşan nesneyi al
        gorev = serializer.save()
        
        print("\n🚀 VIEWSET: YENİ GÖREV KAYDEDİLDİ, MAİL MOTORU BAŞLADI!")
        
        # Atanan personeli ve e-postasını kontrol et
        personel = gorev.atanan_personel
        if personel and hasattr(personel, 'email') and personel.email:
            print(f"📧 Alıcı E-postası: {personel.email}")
            try:
                konu = f"🆕 Yeni Görev Atandı: {gorev.baslik}"
                mesaj = f"Merhaba {personel.first_name},\n\nSana yeni bir görev tanımlandı.\n\n" \
                        f"📌 Başlık: {gorev.baslik}\n" \
                        f"📝 Açıklama: {gorev.aciklama or 'Açıklama girilmemiş.'}\n" \
                        f"📅 Tarih: {gorev.baslangic_tarihi} / {gorev.bitis_tarihi}"
                
                send_mail(
                    subject=konu,
                    message=mesaj,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[personel.email],
                    fail_silently=False,
                )
                print("✅ TEBRİKLER: Mail başarıyla kuyruğa gönderildi!")
            except Exception as e:
                print(f"❌ SMTP HATASI: Mail gönderilemedi. Detay: {e}")
        else:
            print("⚠️ UYARI: Atanan personelin email alanı boş veya geçersiz!")