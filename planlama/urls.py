"""
planlama/urls.py

Projenizin ana urls.py dosyasına şu şekilde dahil edin:

    from django.urls import path, include
    urlpatterns = [
        ...
        path("api/", include("planlama.urls")),
    ]
"""

from rest_framework.routers import DefaultRouter
from .views import GorevViewSet

router = DefaultRouter()
router.register("gorevler", GorevViewSet, basename="gorev")

urlpatterns = router.urls

# Oluşan endpoint'ler:
#   GET    /api/gorevler/            -> kullanıcının görebileceği görevler
#   POST   /api/gorevler/            -> yeni görev ata (sadece yönetici)
#   GET    /api/gorevler/{id}/       -> tek görev detayı
#   POST   /api/gorevler/{id}/tamamla/ -> görevi tamamlandı işaretle
