using Microsoft.AspNetCore.Mvc;
using CatalogAPI.Web.Models;
using CatalogAPI.Web.Services;

namespace CatalogAPI.Web.Controllers;

public class CatalogController : Controller
{
    private readonly ICatalogService _catalogService;

    public CatalogController(ICatalogService catalogService)
    {
        _catalogService = catalogService;
    }

    // GET: /Catalog/Index
    public async Task<IActionResult> Index()
    {
        var items = await _catalogService.GetAllAsync();
        return View(items);
    }

    // GET: /Catalog/Create
    public IActionResult Create()
    {
        return View();
    }

    // POST: /Catalog/Create
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CreateCatalogItemViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var result = await _catalogService.CreateAsync(model);
        if (result)
        {
            return RedirectToAction(nameof(Index));
        }

        ModelState.AddModelError(string.Empty, "Ürün eklenirken API tarafında bir hata oluştu.");
        return View(model);
    }

    // POST: /Catalog/Delete/{id}
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(Guid id)
    {
        await _catalogService.DeleteAsync(id);
        return RedirectToAction(nameof(Index));
    }
}
