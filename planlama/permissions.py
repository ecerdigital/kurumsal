"""
planlama/permissions.py
"""

from rest_framework import permissions


def get_employee(user):
    return getattr(user, "employee", None)


class GorevIzolasyonPermission(permissions.BasePermission):
    """
    Object-level kontrol: bir görev SADECE
      - o görevin atandığı personel, veya
      - aynı tenant içindeki bir yönetici (is_manager=True)
    tarafından görüntülenebilir/işlem yapılabilir.

    Bu sınıf queryset filtresine EK bir güvenlik katmanıdır — queryset zaten
    tenant + kişi bazlı filtrelenmiş olsa da, url'den direkt id denenmesi
    (örn. /gorevler/57/) ihtimaline karşı ikinci bir kilit sağlar.
    """

    def has_object_permission(self, request, view, obj):
        employee = get_employee(request.user)
        if employee is None:
            return False

        # Farklı şirket -> kesinlikle erişim yok
        if obj.tenant_id != employee.tenant_id:
            return False

        # Aynı şirkette ama yönetici değilse, sadece kendi görevini görebilir
        if not getattr(employee, "is_manager", False):
            return obj.atanan_personel_id == employee.id

        return True
