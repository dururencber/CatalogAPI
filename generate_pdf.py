import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>CatalogAPI - Satır Satır Kod ve Mimari Analiz Kitabı</title>
<style>
    @page {
        size: A4;
        margin: 20mm 18mm 20mm 18mm;
        @bottom-right {
            content: counter(page);
        }
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #24292e;
        margin: 0;
        padding: 0;
    }
    h1 {
        color: #0366d6;
        border-bottom: 2px solid #eaecef;
        padding-bottom: 8px;
        margin-top: 30px;
        font-size: 20pt;
        page-break-before: always;
    }
    h1.first-title {
        page-break-before: avoid;
        margin-top: 0;
    }
    h2 {
        color: #1a202c;
        border-bottom: 1px solid #eaecef;
        padding-bottom: 5px;
        margin-top: 24px;
        font-size: 14pt;
    }
    h3 {
        color: #2d3748;
        margin-top: 18px;
        font-size: 12pt;
    }
    pre {
        background-color: #f6f8fa;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 12px;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        font-size: 9.5pt;
        line-height: 1.45;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    code {
        font-family: "SFMono-Regular", Consolas, monospace;
        background-color: #f0f3f6;
        padding: 2px 4px;
        border-radius: 4px;
        font-size: 9pt;
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 9pt;
        font-weight: 600;
        color: white;
        background-color: #2ea44f;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .explanation {
        background-color: #fcfcfc;
        border-left: 4px solid #0366d6;
        padding: 10px 14px;
        margin: 12px 0 20px 0;
        font-size: 10pt;
    }
    .explanation ul {
        margin: 6px 0;
        padding-left: 20px;
    }
    .explanation li {
        margin-bottom: 4px;
    }
    .cover {
        text-align: center;
        padding-top: 120px;
        padding-bottom: 120px;
    }
    .cover h1 {
        border: none;
        font-size: 28pt;
        color: #0366d6;
        margin-bottom: 10px;
    }
    .cover p {
        font-size: 14pt;
        color: #586069;
    }
    .cover .meta {
        margin-top: 60px;
        font-size: 11pt;
        color: #6a737d;
        line-height: 1.8;
    }
</style>
</head>
<body>

<div class="cover">
    <h1>CATALOG API PROJESİ</h1>
    <p>A'dan Z'ye Satır Satır Kod Açıklamaları ve Mimari El Kitabı</p>
    <div class="meta">
        <strong>Teknolojiler:</strong> .NET 10 | Clean Architecture | EF Core | PostgreSQL | JWT & Identity | Docker Compose<br>
        <strong>Geliştirici:</strong> Duru Rençber<br>
        <strong>Tarih:</strong> Ekim 2026
    </div>
</div>

<h1 class="first-title">Bölüm 1: Kimlik Doğrulama ve DTO Modelleri</h1>

<h2>Dosya: CatalogAPI.API/DTOs/AuthDtos.cs</h2>
<span class="badge">API Katmanı / Veri Transfer Nesneleri</span>

<pre>
namespace CatalogAPI.API.DTOs;

public record RegisterDto(string Email, string Password, string Role);
public record LoginDto(string Email, string Password);
public record AuthResponseDto(string Token, string Email, string Role);
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>namespace CatalogAPI.API.DTOs;</code> : Bu sınıfların proje içindeki mantıksal adresini belirtir (C# File-scoped namespace).</li>
        <li><code>public record RegisterDto(...)</code> : Kayıt olacak kullanıcının dışarıdan göndermek zorunda olduğu alanları temsil eder. C#'taki <code>record</code> anahtar kelimesi, değişmez (immutable) ve hafif veri taşıyıcıları üretir.</li>
        <li><code>public record LoginDto(...)</code> : Kullanıcı sisteme girerken yalnızca e-posta ve şifre ister; rol veya ID gibi alanlar kullanıcı tarafından belirlenemez.</li>
        <li><code>public record AuthResponseDto(...)</code> : Başarılı giriş sonrası istemciye (tarayıcıya veya curl'e) geri döneceğimiz veri paketidir. Üretilen JWT token dizesi, kullanıcının e-postası ve yetki seviyesi (rolü) burada yer alır.</li>
    </ul>
</div>

<h1>Bölüm 2: Kimlik Doğrulama Kontrolcüsü (AuthController)</h1>

<h2>Dosya: CatalogAPI.API/Controllers/AuthController.cs</h2>
<span class="badge">API Katmanı / Giriş Kapısı</span>

<pre>
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly UserManager&lt;IdentityUser&gt; _userManager;
    private readonly RoleManager&lt;IdentityRole&gt; _roleManager;
    private readonly IConfiguration _configuration;

    public AuthController(
        UserManager&lt;IdentityUser&gt; userManager,
        RoleManager&lt;IdentityRole&gt; roleManager,
        IConfiguration configuration)
    {
        _userManager = userManager;
        _roleManager = roleManager;
        _configuration = configuration;
    }
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>[ApiController]</code> : ASP.NET Core'a bu sınıfın bir Web API olduğunu bildirir. Model doğrulama (validation) hatalarını otomatik olarak 400 Bad Request şeklinde döner.</li>
        <li><code>[Route("api/[controller]")]</code> : URL rotasını dinamik belirler. Controller adı <code>Auth</code> olduğu için istekler <code>/api/auth</code> adresine yönlenir.</li>
        <li><code>UserManager&lt;IdentityUser&gt;</code> : Microsoft Identity kütüphanesinin kullanıcı oluşturma, şifre hash'leme ve kullanıcı sorgulama motorudur.</li>
        <li><code>RoleManager&lt;IdentityRole&gt;</code> : Sistemdeki rolleri (Admin, User) yöneten servistir.</li>
        <li><code>IConfiguration</code> : <code>appsettings.json</code> veya ortam değişkenlerindeki JWT gizli anahtarlarını okumak için enjekte edilir (Dependency Injection).</li>
    </ul>
</div>

<h3>Kayıt Olma Metodu: Register</h3>
<pre>
    [HttpPost("register")]
    public async Task&lt;IActionResult&gt; Register([FromBody] RegisterDto dto)
    {
        var userExists = await _userManager.FindByEmailAsync(dto.Email);
        if (userExists != null)
            return BadRequest("Bu e-posta adresiyle kayıtlı kullanıcı zaten var.");

        var user = new IdentityUser { UserName = dto.Email, Email = dto.Email };
        var result = await _userManager.CreateAsync(user, dto.Password);

        if (!result.Succeeded)
            return BadRequest(result.Errors);

        if (!await _roleManager.RoleExistsAsync(dto.Role))
            await _roleManager.CreateAsync(new IdentityRole(dto.Role));

        await _userManager.AddToRoleAsync(user, dto.Role);

        return Ok(new { message = "Kullanıcı başarıyla kaydedildi." });
    }
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>[HttpPost("register")]</code> : <code>/api/auth/register</code> adresine gelen POST isteklerini karşılar.</li>
        <li><code>await _userManager.FindByEmailAsync(dto.Email);</code> : Aynı e-posta ile ikinci bir hesap açılmasını engellemek için veritabanında arama yapar.</li>
        <li><code>var result = await _userManager.CreateAsync(user, dto.Password);</code> : Şifreyi asla düz metin (plain text) olarak kaydetmez; PBKDF2 algoritmasıyla tuzlayarak (salt) güvenli hash üretir ve veritabanına yazar.</li>
        <li><code>if (!await _roleManager.RoleExistsAsync(dto.Role))</code> : Kullanıcının talep ettiği rol ("Admin") sistemde henüz tanımlı değilse dinamik olarak oluşturur.</li>
        <li><code>await _userManager.AddToRoleAsync(user, dto.Role);</code> : Kullanıcıyı veritabanında rolüyle ilişkilendirir (`AspNetUserRoles` tablosuna yazar).</li>
    </ul>
</div>

<h3>Giriş Yapma ve Token Üretme Metodu: Login</h3>
<pre>
    [HttpPost("login")]
    public async Task&lt;IActionResult&gt; Login([FromBody] LoginDto dto)
    {
        var user = await _userManager.FindByEmailAsync(dto.Email);
        if (user == null || !await _userManager.CheckPasswordAsync(user, dto.Password))
            return Unauthorized("E-posta veya şifre hatalı.");

        var userRoles = await _userManager.GetRolesAsync(user);
        var role = userRoles.FirstOrDefault() ?? "User";

        var authClaims = new List&lt;Claim&gt;
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id),
            new Claim(ClaimTypes.Email, user.Email!),
            new Claim(ClaimTypes.Role, role),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var authSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_configuration["JwtSettings:SecretKey"]!));

        var token = new JwtSecurityToken(
            issuer: _configuration["JwtSettings:Issuer"],
            audience: _configuration["JwtSettings:Audience"],
            expires: DateTime.UtcNow.AddMinutes(
                Convert.ToDouble(_configuration["JwtSettings:ExpirationInMinutes"])),
            claims: authClaims,
            signingCredentials: new SigningCredentials(authSigningKey, SecurityAlgorithms.HmacSha256)
        );

        return Ok(new AuthResponseDto(new JwtSecurityTokenHandler().WriteToken(token), user.Email!, role));
    }
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>CheckPasswordAsync(...)</code> : Girilen şifreyi veritabanındaki hash ile matematiksel olarak kıyaslar. Uyuşmazsa 401 Unauthorized döner.</li>
        <li><code>authClaims</code> : Token'ın içine gömülecek kimlik bilgileridir (Payload). Kullanıcı ID'si, e-postası ve Rolü burada mühürlenir.</li>
        <li><code>JwtRegisteredClaimNames.Jti</code> : Her token'a benzersiz bir rastgele ID atar (Token replay saldırılarını önlemek için).</li>
        <li><code>SymmetricSecurityKey</code> : <code>appsettings.json</code> içindeki gizli metni baytlara çevirerek simetrik şifreleme anahtarı yapar.</li>
        <li><code>SigningCredentials(..., HmacSha256)</code> : Token'ın üçüncü parçası olan dijital imzayı üretir. İmzayı yalnızca bu sunucu doğrulayabilir.</li>
    </ul>
</div>

<h1>Bölüm 3: Rol Korumalı Ürün Uç Noktaları</h1>

<h2>Dosya: CatalogAPI.API/Controllers/ProductsController.cs</h2>
<span class="badge">API Katmanı / Güvenlik Duvarı</span>

<pre>
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly CatalogDbContext _context;

    public ProductsController(CatalogDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task&lt;IActionResult&gt; GetAll()
    {
        var products = await _context.Products.ToListAsync();
        return Ok(products);
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task&lt;IActionResult&gt; Create([FromBody] CreateProductDto dto)
    {
        var category = await _context.Categories.FindAsync(dto.CategoryId);
        if (category == null)
            return BadRequest("Belirtilen kategori bulunamadı.");

        var product = new Product
        {
            Id = Guid.NewGuid(),
            Name = dto.Name,
            Description = dto.Description,
            Price = dto.Price,
            StockQuantity = dto.Stock,
            CategoryId = dto.CategoryId
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetAll), new { id = product.Id }, product);
    }
}
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>[HttpGet] GetAll()</code> : Üzerinde <code>[Authorize]</code> olmadığı için halka açıktır (public). Vitrindeki ürünleri herkes görebilir.</li>
        <li><code>[Authorize(Roles = "Admin")]</code> : Bu metodun kapısına güvenlik görevlisi koyar. Gelen istekte geçerli bir JWT yoksa <code>401 Unauthorized</code>; token var ama içinde "Admin" rolü yoksa <code>403 Forbidden</code> hatası fırlatır.</li>
        <li><code>var category = await _context.Categories.FindAsync(dto.CategoryId);</code> : İlişkisel bütünlüğü (Referential Integrity) garanti eder. Olmayan bir kategori ID'si ile ürün açılmasını engeller (Yaşadığımız 400 hatasının kaynağı).</li>
        <li><code>await _context.SaveChangesAsync();</code> : EF Core nesne takipçisindeki değişiklikleri PostgreSQL'e <code>INSERT INTO "Products"...</code> SQL sorgusu olarak gönderir.</li>
        <li><code>CreatedAtAction(...)</code> : HTTP 201 Created durum koduyla birlikte `Location` header'ına yeni ürünün adresini ekler.</li>
    </ul>
</div>

<h1>Bölüm 4: Altyapı ve Veritabanı Yapılandırması</h1>

<h2>Dosya: CatalogAPI.Infrastructure/Persistence/CatalogDbContext.cs</h2>
<span class="badge">Infrastructure Katmanı / EF Core</span>

<pre>
namespace CatalogAPI.Infrastructure.Persistence;

public class CatalogDbContext : IdentityDbContext&lt;IdentityUser&gt;
{
    public CatalogDbContext(DbContextOptions&lt;CatalogDbContext&gt; options) : base(options)
    {
    }

    public DbSet&lt;Product&gt; Products =&gt; Set&lt;Product&gt;();
    public DbSet&lt;Category&gt; Categories =&gt; Set&lt;Category&gt;();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity&lt;Product&gt;(entity =&gt;
        {
            entity.HasKey(p =&gt; p.Id);
            entity.Property(p =&gt; p.Name).IsRequired().HasMaxLength(150);
            entity.Property(p =&gt; p.Price).HasPrecision(18, 2);
            entity.HasOne(p =&gt; p.Category)
                  .WithMany(c =&gt; c.Products)
                  .HasForeignKey(p =&gt; p.CategoryId);
        });
    }
}
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>IdentityDbContext&lt;IdentityUser&gt;</code> : Standart DbContext yerine IdentityDbContext'ten miras aldık. Bu sayede veritabanına otomatik olarak `AspNetUsers`, `AspNetRoles`, `AspNetUserClaims` gibi 7 adet güvenlik tablosu eklendi.</li>
        <li><code>base.OnModelCreating(builder);</code> : Identity tablolarının birincil anahtar (Primary Key) eşlemelerinin doğru çalışması için bu satırın ilk sırada çağrılması zorunludur.</li>
        <li><code>entity.Property(p =&gt; p.Price).HasPrecision(18, 2);</code> : Para birimlerinde kuruş hassasiyetini korumak için PostgreSQL tarafında `decimal(18,2)` veri tipini zorunlu kılar.</li>
        <li><code>entity.HasOne(...).WithMany(...)</code> : 1-N (Bire-Çok) ilişki kurar: Bir ürünün tek bir kategorisi olabilir, bir kategoride birden çok ürün bulunabilir.</li>
    </ul>
</div>

<h1>Bölüm 5: Bağımlılık Enjeksiyonu ve Middleware Hattı</h1>

<h2>Dosya: CatalogAPI.API/Program.cs</h2>
<span class="badge">API Katmanı / Uygulama Omurgası</span>

<pre>
var builder = WebApplication.CreateBuilder(args);

// 1. PostgreSQL Veritabanı Bağlantısı
builder.Services.AddDbContext&lt;CatalogDbContext&gt;(options =&gt;
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// 2. Identity Kurulumu
builder.Services.AddIdentity&lt;IdentityUser, IdentityRole&gt;()
    .AddEntityFrameworkStores&lt;CatalogDbContext&gt;()
    .AddDefaultTokenProviders();

// 3. JWT Kimlik Doğrulama Şeması
builder.Services.AddAuthentication(options =&gt;
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =&gt;
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = builder.Configuration["JwtSettings:Issuer"],
        ValidAudience = builder.Configuration["JwtSettings:Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(builder.Configuration["JwtSettings:SecretKey"]!))
    };
});

var app = builder.Build();

app.UseAuthentication(); // 1. Sen kimsin? (Token çözülür)
app.UseAuthorization();  // 2. Buraya girmeye yetkin var mı? (Rol kontrol edilir)

app.MapControllers();
app.Run();
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>builder.Services.AddDbContext...</code> : Veritabanı bağlantı havuzunu (connection pool) oluşturur ve Controller'ların constructor'larında DbContext talep edebilmesini sağlar.</li>
        <li><code>AddEntityFrameworkStores&lt;CatalogDbContext&gt;()</code> : Identity motorunun kullanıcı verilerini dosya veya belleğe değil, bizim PostgreSQL tablolarımıza yazmasını sağlar.</li>
        <li><code>options.TokenValidationParameters</code> : Gelen her istekte token'ın süresinin dolup dolmadığını (`ValidateLifetime`), sunucu imzasının doğruluğunu (`ValidateIssuerSigningKey`) otomatik test eder.</li>
        <li><code>app.UseAuthentication() ve app.UseAuthorization()</code> : Sıralama hayatidir! Önce kimlik doğrulanmalı (`Authentication`), ardından yetki sorgulanmalıdır (`Authorization`). Sıralama ters olursa yetkilendirme her zaman başarısız olur.</li>
    </ul>
</div>

<h1>Bölüm 6: Konteynerleştirme ve Orkestrasyon</h1>

<h2>Dosya: CatalogAPI.API/Dockerfile</h2>
<span class="badge">DevOps / Multi-Stage Build</span>

<pre>
# 1. Aşama: Build & Publish (SDK İmajı - ~1 GB)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /app

# Katman csproj dosyalarını kopyala ve restore et (Docker Cache Optimizasyonu)
COPY CatalogAPI.Domain/*.csproj CatalogAPI.Domain/
COPY CatalogAPI.Application/*.csproj CatalogAPI.Application/
COPY CatalogAPI.Infrastructure/*.csproj CatalogAPI.Infrastructure/
COPY CatalogAPI.API/*.csproj CatalogAPI.API/

RUN dotnet restore CatalogAPI.API/CatalogAPI.API.csproj

# Kalan tüm kodları kopyala ve derle
COPY . .
WORKDIR /app/CatalogAPI.API
RUN dotnet publish -c Release -o /app/out

# 2. Aşama: Runtime (Hafif ASP.NET İmajı - ~150 MB)
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/out .

EXPOSE 8080
ENTRYPOINT ["dotnet", "CatalogAPI.API.dll"]
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>FROM ... AS build</code> : Derleme için ağır olan SDK imajını geçici bir aşama olarak tanımlar.</li>
        <li><code>COPY .../*.csproj ...</code> ve <code>RUN dotnet restore</code> : Kodlar değişse bile NuGet paketleri değişmediği sürece Docker bu adımı önbellekten (cache) alır. Böylece her derlemede internetten kütüphane indirilmez.</li>
        <li><code>RUN dotnet publish -c Release -o /app/out</code> : Kodları optimize edilmiş, üretime hazır binary DLL'ler haline getirir ve `/app/out` dizinine çıkarır.</li>
        <li><code>COPY --from=build /app/out .</code> : Ağır SDK aşamasındaki kod ve derleme çöplerini çöpe atar; sadece derlenmiş DLL'leri hafif Runtime imajına taşır. İmaj boyutu %80 küçülür.</li>
    </ul>
</div>

<h2>Dosya: docker-compose.yml</h2>
<span class="badge">DevOps / Servis Orkestrasyonu</span>

<pre>
services:
  db:
    image: postgres:16-alpine
    container_name: catalog_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: CatalogDb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  catalog-api:
    build:
      context: .
      dockerfile: CatalogAPI.API/Dockerfile
    container_name: catalog_api
    restart: always
    depends_on:
      - db
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=db;Port=5432;Database=CatalogDb;Username=postgres;Password=postgres
      - JwtSettings__Issuer=CatalogAPI
      - JwtSettings__Audience=CatalogAppUsers
      - JwtSettings__SecretKey=BuCokGizliVeGucluBirAnahtardirEnAz32KarakterOlmali!
      - JwtSettings__ExpirationInMinutes=60
    ports:
      - "5054:8080"

  catalog-web:
    build:
      context: .
      dockerfile: CatalogAPI.Web/Dockerfile
    container_name: catalog_web
    restart: always
    depends_on:
      - catalog-api
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ApiSettings__BaseUrl=http://catalog-api:8080/
    ports:
      - "5001:8080"

volumes:
  postgres_data:
</pre>

<div class="explanation">
    <strong>Satır Satır Açıklama:</strong>
    <ul>
        <li><code>services: db</code> : PostgreSQL veritabanını izole container olarak ayağa kaldırır. Alpine tabanlı hafif imaj kullanır.</li>
        <li><code>volumes: postgres_data</code> : Container silinse veya yeniden başlatılsa dahi verilerin (kullanıcılar, ürünler) kaybolmaması için Docker üzerinde kalıcı disk alanı bağlar.</li>
        <li><code>depends_on: - db</code> : `catalog-api` başlamadan önce mutlaka `db` servisinin ayağa kalkmasını garanti eder.</li>
        <li><code>Host=db</code> : API, veritabanına bağlanırken `localhost` yerine Docker iç ağındaki container adı olan `db` ismini kullanır. Docker bu adı arka planda otomatik IP adresine çözümler.</li>
        <li><code>ports: - "5054:8080"</code> : Host makinenin (Mac) 5054 portunu, container içindeki Kestrel web sunucusunun dinlediği 8080 portuna yönlendirir.</li>
        <li><code>ApiSettings__BaseUrl=http://catalog-api:8080/</code> : Web (MVC) katmanının API ile doğrudan Docker iç ağı üzerinden yüksek hızda konuşmasını sağlar.</li>
    </ul>
</div>

</body>
</html>
"""

with open("CatalogAPI_Rehber.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML kitapçığı oluşturuldu: CatalogAPI_Rehber.html")
print("PDF üretiliyor...")

# macOS yerleşik headless browser ile PDF üretme
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if os.path.exists(chrome_path):
    subprocess.run([
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf=CatalogAPI_Egitim_Kitabi.pdf",
        "CatalogAPI_Rehber.html"
    ])
    print("BAŞARILI: 'CatalogAPI_Egitim_Kitabi.pdf' Mac'inde oluşturuldu!")
else:
    print("Bilgi: Safari/Finder üzerinden doğrudan açılıyor...")
    subprocess.run(["open", "CatalogAPI_Rehber.html"])

