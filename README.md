📦 CatalogAPI

Modern RESTful mimari standartlarına uygun, JWT ile yetkilendirilmiş, Entity Framework Core ile veri yönetimi sağlayan ve Docker ortamına hazır bir Ürün Kataloğu API servisidir.

🎯 Projenin Amacı ve Özellikleri

Bu proje, kurumsal backend geliştirme pratiklerini ve bulut odaklı konteynerizasyon süreçlerini uygulamak amacıyla tasarlanmıştır:

RESTful Standartları: Kaynak odaklı URL yapısı, doğru HTTP metotları (GET, POST, PUT, DELETE) ve durum kodları (200, 201, 400, 401, 404).

Katmanlı / Güvenli Veri Akışı: Entity modellerinin dış dünyaya kapatılarak DTO (Data Transfer Object) deseni ile veri taşınması.

Durumsuz (Stateless) Kimlik Doğrulama: JSON Web Token (JWT) tabanlı authentication ve rol bazlı authorization ([Authorize]).

Veritabanı Yönetimi: PostgreSQL üzerinde Code-First yaklaşımı ve Entity Framework Core migration mekanizması.

Konteyner Desteği: Multi-stage Dockerfile ile platformdan bağımsız derleme ve dağıtım hazırlığı.

Etkileşimli Dokümantasyon: JWT Bearer entegrasyonuna sahip Swagger UI.

🏗️ Mimari & Teknoloji Yığını

Çalışma Ortamı: C# / .NET 8 Web API

Veritabanı & ORM: PostgreSQL / Entity Framework Core (Npgsql)

Kimlik Doğrulama: Microsoft.AspNetCore.Authentication.JwtBearer

Dokümantasyon: Swashbuckle / Swagger OpenAPI

Konteyner: Docker

📁 Dizin Yapısı

CatalogAPI/
├── Controllers/         # API Endpoint tanımlamaları ve istek karşılama
├── Models/              # Veritabanı tablolarına karşılık gelen Entity sınıfları
│   ├── Entities/        # Temel veritabanı modelleri (Product, User vb.)
│   └── DTOs/            # Dış dünyaya sunulan veri aktarım nesneleri
├── Data/                # DbContext ve veritabanı konfigürasyonları
│   └── AppDbContext.cs
├── Services/            # İş mantığı ve token üretim servisleri
├── Migrations/          # EF Core veritabanı göç geçmişi
├── Dockerfile           # Konteyner derleme adımları
├── appsettings.json     # Genel uygulama yapılandırma şablonu
└── Program.cs           # Dependency Injection ve Middleware hattı


💻 Yerel Geliştirme Ortamı Kurulumu

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

Gereksinimler

.NET 8 SDK

Docker Desktop (veya yerel PostgreSQL sunucusu)

Git

1. Repoyu Klonlayın

git clone https://github.com/<kullanici-adiniz>/CatalogAPI.git
cd CatalogAPI


2. Yerel Veritabanını Başlatın (Docker)

PostgreSQL instance'ını arka planda ayağa kaldırmak için:

docker run --name catalog-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=CatalogDb \
  -p 5432:5432 \
  -d postgres:16-alpine


3. Gizli Bilgileri Tanımlayın (.NET User Secrets)

Hassas verileri (şifre ve JWT secret key) kodun içerisine yazmadan yerel geliştirme kasanıza ekleyin:

dotnet user-secrets init

# Veritabanı bağlantı dizesi
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Host=localhost;Port=5432;Database=CatalogDb;Username=postgres;Password=postgres"

# JWT konfigürasyonu
dotnet user-secrets set "JwtSettings:Secret" "BuKisimEnAz32KarakterliCokGizliBirKeyOlmali123!"
dotnet user-secrets set "JwtSettings:Issuer" "CatalogAPI"
dotnet user-secrets set "JwtSettings:Audience" "CatalogAPIUsers"


4. Veritabanı Migration İşlemini Uygulayın

Veritabanı şemasını PostgreSQL üzerinde oluşturmak için:

dotnet ef database update


(Eğer dotnet ef komutu yüklü değilse: dotnet tool install --global dotnet-ef)

5. Uygulamayı Çalıştırın

dotnet run


Uygulama çalıştıktan sonra API testlerini gerçekleştirmek için tarayıcınızdan Swagger arayüzüne gidin:
👉 https://localhost:5001/swagger veya http://localhost:5000/swagger

🔑 API Kimlik Doğrulama Akışı

/api/auth/register veya /api/auth/login endpoint'ine geçerli bilgileri göndererek JWT Token elde edin.

Swagger ekranının sağ üst köşesindeki Authorize butonuna tıklayın.

Açılan kutucuğa format şu şekilde olacak şekilde token'ı girin:

Bearer <sizin_token_degeriniz>


Artık kilitli ([Authorize]) endpoint'lere (POST, PUT, DELETE /api/products) istek atabilirsiniz.

🐳 Docker ile Çalıştırma

Projeyi bağımsız bir imaj olarak paketleyip çalıştırmak için:

# İmajı derleyin
docker build -t catalog-api .

# Konteyneri başlatın
docker run -d -p 8080:8080 --name catalog-app catalog-api


📄 Lisans

Bu proje eğitim ve portfolyo amacıyla hazırlanmıştır. Açık kaynak olarak geliştirilebilir.
