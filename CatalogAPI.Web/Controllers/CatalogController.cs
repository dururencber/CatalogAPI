using CatalogAPI.Web.Models;
using CatalogAPI.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace CatalogAPI.Web.Controllers;

public class CatalogController : Controller
{
    private readonly ICatalogService _catalogService;
    // Veritabanındaki 'Elektronik' kategorisinin ID'si
    private static readonly Guid DefaultCategoryId = Guid.Parse("db59aabf-04b3-450d-b5e5-b6bce320d0a3");

    public CatalogController(ICatalogService catalogService)
    {
        _catalogService = catalogService;
    }

    public async Task<IActionResult> Index()
    {
        var items = await _catalogService.GetAllAsync();
        return View(items);
    }

    public IActionResult Create()
    {
        // CategoryId'si dolu bir model gönderiyoruz
        var model = new CreateCatalogItemViewModel
        {
            CategoryId = DefaultCategoryId
        };
        return View(model);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CreateCatalogItemViewModel model)
    {
        if (model.CategoryId == Guid.Empty)
        {
            model.CategoryId = DefaultCategoryId;
        }

        if (!ModelState.IsValid)
            return View(model);

        var result = await _catalogService.CreateAsync(model);
        if (result)
            return RedirectToAction(nameof(Index));

        ModelState.AddModelError(string.Empty, "Ürün eklenirken API tarafında bir hata oluştu.");
        return View(model);
    }

    public async Task<IActionResult> Edit(Guid id)
    {
        var item = await _catalogService.GetByIdAsync(id);
        if (item == null)
            return NotFound();

        return View(item);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(Guid id, CatalogItemViewModel model)
    {
        if (id != model.Id)
            return BadRequest();

        if (!ModelState.IsValid)
            return View(model);

        var result = await _catalogService.UpdateAsync(id, model);
        if (result)
            return RedirectToAction(nameof(Index));

        ModelState.AddModelError(string.Empty, "Ürün güncellenirken API tarafında bir hata oluştu.");
        return View(model);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(Guid id)
    {
        await _catalogService.DeleteAsync(id);
        return RedirectToAction(nameof(Index));
    }
}
