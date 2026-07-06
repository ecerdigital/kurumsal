# Yetkilendirme Sistemi Kurulum Rehberi

## 📋 Genel Bakış

Bu sistem, her şirketin kendi **Roller** tanımlaması ve bu rollere **İzinler** atayarak personellerin erişimini kontrol etmesini sağlar.

## 🏗️ Migrasyonları Çalıştır

```bash
python manage.py makemigrations
python manage.py migrate
```

## 👤 Admin Panelinde İlk Kurulum

1. **Django Admin**'e giriş yap: `http://localhost:8000/admin/`
2. **Roller** sekmesine git
3. Şirket için yeni roller oluştur (örn: "Müdür", "Muhasebeci", "Stajyer")

### Örnek Rol Oluşturma

| Rol Adı | İzinler |
|---------|---------|
| **Müdür** | Tüm İzinler |
| **Muhasebeci** | `muhasebe_goruntule`, `muhasebe_islem` |
| **Stajyer** | `personel_goruntule` |

## 🔐 API Endpoints

### Personel Yönetimi

```
GET    /api/personel/              → Personel listesi
POST   /api/personel/              → Personel ekle (personel_ekle izni)
PUT    /api/personel/{id}/         → Personel güncelle
DELETE /api/personel/{id}/         → Personel sil (personel_sil izni)
```

### Rol Atama

```
POST /api/personel/{id}/assign-role/
Content-Type: application/json

{
    "role_id": 1
}
```

### İzinleri Al

```
GET /api/personel/my-permissions/

Response:
{
    "user_type": "Personel",
    "role": {
        "id": 1,
        "name": "Müdür",
        "permissions": [...]
    },
    "permissions": [
        "personel_ekle",
        "personel_sil",
        "personel_goruntule",
        ...
    ]
}
```

### Roller Yönetimi

```
GET    /api/roles/          → Tüm roller
POST   /api/roles/          → Yeni rol oluştur
PUT    /api/roles/{id}/     → Rol güncelle
DELETE /api/roles/{id}/     → Rol sil
```

## 📊 Veritabanı Modelleri

### Role
```python
- tenant (ForeignKey)
- name (CharField)
- description (TextField)
- created_at (DateTimeField)
```

### Permission
```python
- role (ForeignKey)
- permission_code (CharField)
  - personel_ekle
  - personel_sil
  - personel_goruntule
  - muhasebe_goruntule
  - muhasebe_islem
  - planlama_goruntule
  - planlama_islem
```

### EmployeeRole
```python
- employee (OneToOneField)
- role (ForeignKey)
- assigned_at (DateTimeField)
- assigned_by (ForeignKey to CustomUser)
```

## 🎯 Frontend Entegrasyonu

### İzin Kontrolü

```javascript
const hasPermission = (permission) => {
    return userPermissions.includes(permission);
};

// Kullanım
{hasPermission('personel_ekle') && (
    <button>Personel Ekle</button>
)}
```

### İzinleri Al

```javascript
const fetchUserPermissions = () => {
    axios.get('http://localhost:8000/api/personel/my-permissions/', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => {
        setUserPermissions(res.data.permissions);
    });
};
```

## 🔒 Erişim Kontrolleri

### Personel Listesi
- ✅ Yetkili: `personel_goruntule` izni olan kullanıcılar
- ❌ Yetkisiz: 403 Forbidden

### Personel Ekleme
- ✅ Yetkili: `personel_ekle` izni olan kullanıcılar
- ❌ Yetkisiz: 403 Forbidden

### Personel Silme
- ✅ Yetkili: `personel_sil` izni olan kullanıcılar
- ❌ Yetkisiz: 403 Forbidden

## 💾 Örnek Curl Komutları

### Token Al
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "password"}'
```

### İzinleri Al
```bash
curl -X GET http://localhost:8000/api/personel/my-permissions/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Personele Rol Ata
```bash
curl -X POST http://localhost:8000/api/personel/1/assign-role/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role_id": 2}'
```

## ⚙️ Ayarlar (settings.py)

Eğer Custom Authentication kullanıyorsanız, aşağıdakiler zaten yapılandırılmış olmalıdır:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'personel',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

## 🚀 Sonraki Adımlar

1. **Muhasebe ve Planlama** modüllerine benzer yetkilendirme ekle
2. **Middleware** oluşturarak tüm modüllerden izin kontrolü yap
3. **Denetim Günlüğü** (Audit Log) ekle - kim ne yaptığını takip et
4. **Rol Şablonları** oluştur - hazır rol setleri sun

---

✅ **Sistem hazır! Şimdi her personele rol atayabilir ve onların erişimini kontrol edebilirsin.**
