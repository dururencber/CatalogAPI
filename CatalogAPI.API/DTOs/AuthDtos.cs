namespace CatalogAPI.API.DTOs;

public record RegisterRequestDto(string Email, string Password, string Role = "User");
public record LoginRequestDto(string Email, string Password);
public record AuthResponseDto(string Token, string Email, string Role);
