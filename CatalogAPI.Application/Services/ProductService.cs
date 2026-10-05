using CatalogAPI.Application.DTOs.Products;
using CatalogAPI.Application.Interfaces;
using CatalogAPI.Application.Interfaces.Services;
using CatalogAPI.Domain.Entities;

namespace CatalogAPI.Application.Services;

public class ProductService : IProductService
{
    private readonly IProductRepository _productRepository;
    private readonly ICategoryRepository _categoryRepository;

    public ProductService(IProductRepository productRepository, ICategoryRepository categoryRepository)
    {
        _productRepository = productRepository;
        _categoryRepository = categoryRepository;
    }

    public async Task<IReadOnlyList<ProductDto>> GetAllProductsAsync()
    {
        var products = await _productRepository.GetAllAsync();
        return products.Select(p => new ProductDto
        {
            Id = p.Id,
            Name = p.Name,
            Description = p.Description,
            Price = p.Price,
            StockQuantity = p.StockQuantity,
            CategoryId = p.CategoryId
        }).ToList();
    }

    public async Task<ProductDto?> GetProductByIdAsync(Guid id)
    {
        var product = await _productRepository.GetByIdAsync(id);
        if (product == null) return null;

        return new ProductDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price,
            StockQuantity = product.StockQuantity,
            CategoryId = product.CategoryId
        };
    }

    public async Task<IReadOnlyList<ProductDto>> GetProductsByCategoryIdAsync(Guid categoryId)
    {
        var products = await _productRepository.GetByCategoryIdAsync(categoryId);
        return products.Select(p => new ProductDto
        {
            Id = p.Id,
            Name = p.Name,
            Description = p.Description,
            Price = p.Price,
            StockQuantity = p.StockQuantity,
            CategoryId = p.CategoryId
        }).ToList();
    }

    public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
    {
        var category = await _categoryRepository.GetByIdAsync(dto.CategoryId);
        if (category == null)
            throw new ArgumentException("Belirtilen kategori bulunamadı.");

        var product = new Product
        {
            Id = Guid.NewGuid(),
            Name = dto.Name,
            Description = dto.Description,
            Price = dto.Price,
            StockQuantity = dto.StockQuantity,
            CategoryId = dto.CategoryId,
            CreatedAt = DateTime.UtcNow
        };

        var created = await _productRepository.AddAsync(product);

        return new ProductDto
        {
            Id = created.Id,
            Name = created.Name,
            Description = created.Description,
            Price = created.Price,
            StockQuantity = created.StockQuantity,
            CategoryId = created.CategoryId
        };
    }

    public async Task<bool> UpdateProductAsync(Guid id, UpdateProductDto dto)
    {
        var product = await _productRepository.GetByIdAsync(id);
        if (product == null) return false;

        var category = await _categoryRepository.GetByIdAsync(dto.CategoryId);
        if (category == null)
            throw new ArgumentException("Belirtilen kategori bulunamadı.");

        product.Name = dto.Name;
        product.Description = dto.Description;
        product.Price = dto.Price;
        product.StockQuantity = dto.StockQuantity;
        product.CategoryId = dto.CategoryId;

        await _productRepository.UpdateAsync(product);
        return true;
    }

    public async Task<bool> DeleteProductAsync(Guid id)
    {
        var product = await _productRepository.GetByIdAsync(id);
        if (product == null) return false;

        await _productRepository.DeleteAsync(product);
        return true;
    }
}
