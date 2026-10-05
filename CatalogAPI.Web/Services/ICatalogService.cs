using CatalogAPI.Web.Models;

namespace CatalogAPI.Web.Services;

public interface ICatalogService
{
    Task<List<CatalogItemViewModel>> GetAllAsync();
    Task<CatalogItemViewModel?> GetByIdAsync(Guid id);
    Task<bool> CreateAsync(CreateCatalogItemViewModel model);
    Task<bool> UpdateAsync(Guid id, CatalogItemViewModel model);
    Task<bool> DeleteAsync(Guid id);
}
