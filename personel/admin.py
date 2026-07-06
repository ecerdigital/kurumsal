from django.contrib import admin
from .models import Employee, Role, Permission, EmployeeRole

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tenant', 'position', 'email', 'get_role')
    list_filter = ('tenant', 'position')
    search_fields = ('first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        try:
            return obj.role_assignment.role.name if obj.role_assignment and obj.role_assignment.role else '—'
        except:
            return '—'
    get_role.short_description = 'Rol'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'get_permission_count', 'created_at')
    list_filter = ('tenant', 'created_at')
    search_fields = ('name',)
    
    def get_permission_count(self, obj):
        return obj.permissions.count()
    get_permission_count.short_description = 'İzin Sayısı'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission_code', 'get_permission_display')
    list_filter = ('role__tenant', 'permission_code')
    search_fields = ('role__name', 'permission_code')
    
    def get_permission_display(self, obj):
        return obj.get_permission_code_display()
    get_permission_display.short_description = 'İzin Açıklaması'


@admin.register(EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'role', 'assigned_at', 'assigned_by')
    list_filter = ('role__tenant', 'assigned_at')
    search_fields = ('employee__first_name', 'employee__last_name', 'role__name')
    readonly_fields = ('assigned_at',)
