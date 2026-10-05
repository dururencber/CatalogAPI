using CatalogAPI.Domain.Entities;

namespace CatalogAPI.Application.Interfaces;

public interface IProductRepository
{
    Task<IReadOnlyList<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(Guid id);
    Task<IReadOnlyList<Product>> GetByCategoryIdAsync(Guid categoryId);
    Task<Product> AddAsync(Product product);
    Task UpdateAsync(Product product);
    Task DeleteAsync(Product product);
}
