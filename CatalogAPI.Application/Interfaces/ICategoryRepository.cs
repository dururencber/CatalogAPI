using CatalogAPI.Domain.Entities;

namespace CatalogAPI.Application.Interfaces;

public interface ICategoryRepository
{
    Task<IReadOnlyList<Category>> GetAllAsync();
    Task<Category?> GetByIdAsync(Guid id);
    Task AddAsync(Category category);
    void Update(Category category);
    void Delete(Category category);
    Task<bool> SaveChangesAsync();
}