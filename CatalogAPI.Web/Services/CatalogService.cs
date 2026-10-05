using System.Net.Http.Json;
using CatalogAPI.Web.Models;

namespace CatalogAPI.Web.Services;

public class CatalogService : ICatalogService
{
    private readonly HttpClient _httpClient;

    public CatalogService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<List<CatalogItemViewModel>> GetAllAsync()
    {
        var response = await _httpClient.GetFromJsonAsync<List<CatalogItemViewModel>>("api/Products");
        return response ?? new List<CatalogItemViewModel>();
    }

    public async Task<CatalogItemViewModel?> GetByIdAsync(Guid id)
    {
        return await _httpClient.GetFromJsonAsync<CatalogItemViewModel>($"api/Products/{id}");
    }

    public async Task<bool> CreateAsync(CreateCatalogItemViewModel model)
    {
        var response = await _httpClient.PostAsJsonAsync("api/Products", model);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> UpdateAsync(Guid id, CatalogItemViewModel model)
    {
        var response = await _httpClient.PutAsJsonAsync($"api/Products/{id}", model);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        var response = await _httpClient.DeleteAsync($"api/Products/{id}");
        return response.IsSuccessStatusCode;
    }
}
