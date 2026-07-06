from django.db import models
from core.models import Tenant # Core modülündeki Şirket yapısını çağırıyoruz

class Employee(models.Model):
    # MULTI-TENANCY: Bu personel hangi şirketin çalışanı?
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="employees")
    
    first_name = models.CharField(max_length=100, verbose_name="Adı")
    last_name = models.CharField(max_length=100, verbose_name="Soyadı")
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefonu")
    position = models.CharField(max_length=100, verbose_name="Pozisyonu / Görevi")
    hire_date = models.DateField(auto_now_add=True, verbose_name="İşe Giriş Tarihi")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maaşı")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.tenant.name})"

# ===== YENİ: YETKİLENDİRME SİSTEMİ =====

class Role(models.Model):
    """
    Her şirketin kendine ait roller/pozisyonlar tanımlayabileceği model.
    Örn: "Müdür", "Muhasebeci", "Stajyer"
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100, verbose_name="Rol Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('tenant', 'name')
        verbose_name_plural = "Roller"
    
    def __str__(self):
        return f"{self.tenant.name} - {self.name}"


class Permission(models.Model):
    """
    Yetkilendirme sistemi: Her rolle ilişkilendirilmiş izinler.
    """
    PERMISSION_CHOICES = (
        ('personel_ekle', 'Personel Ekleme'),
        ('personel_sil', 'Personel Silme'),
        ('personel_goruntule', 'Personel Listesini Görüntüleme'),
        ('muhasebe_goruntule', 'Muhasebe Sayfasını Görüntüleme'),
        ('muhasebe_islem', 'Muhasebe İşlem Yapma'),
        ('planlama_goruntule', 'Planlama Sayfasını Görüntüleme'),
        ('planlama_islem', 'Planlama İşlem Yapma'),
    )
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission_code = models.CharField(max_length=50, choices=PERMISSION_CHOICES)
    
    class Meta:
        unique_together = ('role', 'permission_code')
        verbose_name_plural = "İzinler"
    
    def __str__(self):
        return f"{self.role.name} - {self.get_permission_code_display()}"


class EmployeeRole(models.Model):
    """
    Her personele atanmış roller. Bir personel birden fazla role sahip olabilir.
    """
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='role_assignment')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.role.name if self.role else 'Rol Yok'}"
    
    @property
    def permissions(self):
        """Personelin tüm izinlerini döndür"""
        if not self.role:
            return Permission.objects.none()
        return self.role.permissions.all()
    
    def has_permission(self, permission_code):
        """Personelin belirli bir izni var mı kontrol et"""
        return self.permissions.filter(permission_code=permission_code).exists()


# Eski model (Backward compatibility için yorum içinde bıraktım)
# class PositionPermission(models.Model):
#     tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='position_permissions')
#     position_name = models.CharField(max_length=100)
#     can_view_employees = models.BooleanField(default=True, verbose_name="Personelleri Görüntüleyebilir")
#     can_add_employee = models.BooleanField(default=False, verbose_name="Personel Ekleyebilir")
#     can_edit_employee = models.BooleanField(default=False, verbose_name="Personel Düzenleyebilir")
#     can_delete_employee = models.BooleanField(default=False, verbose_name="Personel Silebilir")
#     can_view_salary = models.BooleanField(default=False, verbose_name="Maaş Bilgisini Görebilir")
#
#     class Meta:
#         unique_together = ('tenant', 'position_name')
#
#     def __str__(self):
#         return f"{self.tenant.name} - {self.position_name} Yetkileri"
