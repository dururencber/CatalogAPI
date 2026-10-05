using CatalogAPI.Domain.Entities;

namespace CatalogAPI.Application.Interfaces;

public interface IProductRepository
{
    Task<IReadOnlyList<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(Guid id);
    Task<IReadOnlyList<Product>> GetByCategoryIdAsync(Guid categoryId);
    Task AddAsync(Product product);
    void Update(Product product);
    void Delete(Product product);
    Task<bool> SaveChangesAsync();
}