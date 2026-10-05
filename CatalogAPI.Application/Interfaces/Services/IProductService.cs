using CatalogAPI.Application.DTOs.Products;

namespace CatalogAPI.Application.Interfaces.Services;

public interface IProductService
{
    Task<IReadOnlyList<ProductDto>> GetAllProductsAsync();
    Task<ProductDto?> GetProductByIdAsync(Guid id);
    Task<IReadOnlyList<ProductDto>> GetProductsByCategoryIdAsync(Guid categoryId);
    Task<ProductDto> CreateProductAsync(CreateProductDto dto);
    Task<bool> UpdateProductAsync(Guid id, UpdateProductDto dto);
    Task<bool> DeleteProductAsync(Guid id);
}
