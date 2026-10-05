using CatalogAPI.Application.Interfaces.Services;
using CatalogAPI.Application.Services;
using Microsoft.Extensions.DependencyInjection;

namespace CatalogAPI.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        services.AddScoped<ICategoryService, CategoryService>();
        services.AddScoped<IProductService, ProductService>();

        return services;
    }
}