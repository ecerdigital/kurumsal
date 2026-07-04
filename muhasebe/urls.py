from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinanceEntryViewSet

router = DefaultRouter()
router.register(r'finance', FinanceEntryViewSet, basename='financeentry')

urlpatterns = [
    path('', include(router.urls)),
]