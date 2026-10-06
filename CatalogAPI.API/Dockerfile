# 1. Aşama: Build & Publish (SDK İmajı)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /app

# Katman csproj dosyalarını kopyala ve restore et (Önbellekleme için)
COPY CatalogAPI.Domain/*.csproj CatalogAPI.Domain/
COPY CatalogAPI.Application/*.csproj CatalogAPI.Application/
COPY CatalogAPI.Infrastructure/*.csproj CatalogAPI.Infrastructure/
COPY CatalogAPI.API/*.csproj CatalogAPI.API/

RUN dotnet restore CatalogAPI.API/CatalogAPI.API.csproj

# Kalan tüm kaynak kodları kopyala ve yayınla
COPY . .
WORKDIR /app/CatalogAPI.API
RUN dotnet publish -c Release -o /app/out

# 2. Aşama: Runtime (Hafif ASP.NET İmajı)
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/out .

EXPOSE 8080
ENTRYPOINT ["dotnet", "CatalogAPI.API.dll"]
