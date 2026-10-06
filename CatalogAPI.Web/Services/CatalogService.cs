using System.Net.Http.Headers;
using System.Net.Http.Json;
using CatalogAPI.Web.Models;

namespace CatalogAPI.Web.Services;

public class CatalogService : ICatalogService
{
    private readonly HttpClient _httpClient;
    private string? _cachedToken;

    public CatalogService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    private async Task EnsureAuthenticatedAsync()
    {
        if (!string.IsNullOrEmpty(_cachedToken))
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _cachedToken);
            return;
        }

        try
        {
            var loginPayload = new { email = "admin@catalog.com", password = "Password123!" };
            var response = await _httpClient.PostAsJsonAsync("api/auth/login", loginPayload);
            if (response.IsSuccessStatusCode)
            {
                var authResult = await response.Content.ReadFromJsonAsync<LoginResult>();
                if (authResult != null && !string.IsNullOrEmpty(authResult.Token))
                {
                    _cachedToken = authResult.Token;
                    _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _cachedToken);
                }
            }
        }
        catch
        {
            // Login başarısız olursa normal devam et
        }
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
        await EnsureAuthenticatedAsync();
        var response = await _httpClient.PostAsJsonAsync("api/Products", model);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> UpdateAsync(Guid id, CatalogItemViewModel model)
    {
        await EnsureAuthenticatedAsync();
        var response = await _httpClient.PutAsJsonAsync($"api/Products/{id}", model);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        await EnsureAuthenticatedAsync();
        var response = await _httpClient.DeleteAsync($"api/Products/{id}");
        return response.IsSuccessStatusCode;
    }

    private record LoginResult(string Token, string Email, string Role);
}
