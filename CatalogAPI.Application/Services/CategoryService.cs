using CatalogAPI.Application.DTOs.Categories;
using CatalogAPI.Application.Interfaces;
using CatalogAPI.Application.Interfaces.Services;
using CatalogAPI.Domain.Entities;

namespace CatalogAPI.Application.Services;

public class CategoryService : ICategoryService
{
    private readonly ICategoryRepository _categoryRepository;

    public CategoryService(ICategoryRepository categoryRepository)
    {
        _categoryRepository = categoryRepository;
    }

    public async Task<IReadOnlyList<CategoryDto>> GetAllCategoriesAsync()
    {
        var categories = await _categoryRepository.GetAllAsync();

        // Entity -> DTO Dönüşümü (Mapping)
        return categories.Select(c => new CategoryDto
        {
            Id = c.Id,
            Name = c.Name
        }).ToList();
    }

    public async Task<CategoryDto?> GetCategoryByIdAsync(Guid id)
    {
        var category = await _categoryRepository.GetByIdAsync(id);
        if (category == null) return null;

        return new CategoryDto
        {
            Id = category.Id,
            Name = category.Name
        };
    }

    public async Task<CategoryDto> CreateCategoryAsync(CreateCategoryDto dto)
    {
        // 1. DTO'dan yeni bir Domain Entity nesnesi üretiyoruz
        var category = new Category
        {
            Id = Guid.NewGuid(),
            Name = dto.Name
        };

        // 2. Veritabanına eklemesi için Repository'ye veriyoruz
        await _categoryRepository.AddAsync(category);
        await _categoryRepository.SaveChangesAsync();

        // 3. Eklenen kaydın DTO halini dışarıya dönüyoruz
        return new CategoryDto
        {
            Id = category.Id,
            Name = category.Name
        };
    }

    public async Task<bool> DeleteCategoryAsync(Guid id)
    {
        var category = await _categoryRepository.GetByIdAsync(id);
        if (category == null) return false;

        _categoryRepository.Delete(category);
        return await _categoryRepository.SaveChangesAsync();
    }
}