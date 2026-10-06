# 1. Aşama: Build & Publish
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /app

COPY CatalogAPI.Web/*.csproj CatalogAPI.Web/
RUN dotnet restore CatalogAPI.Web/CatalogAPI.Web.csproj

COPY CatalogAPI.Web/. CatalogAPI.Web/
WORKDIR /app/CatalogAPI.Web
RUN dotnet publish -c Release -o /app/out

# 2. Aşama: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/out .

EXPOSE 8080
ENTRYPOINT ["dotnet", "CatalogAPI.Web.dll"]
