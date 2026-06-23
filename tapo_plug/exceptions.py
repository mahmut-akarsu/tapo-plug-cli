class TapoPlugError(Exception):
    """Tapo priz yapilandirma veya baglanti hatasi."""


class TapoConfigError(TapoPlugError):
    """Eksik veya gecersiz yapilandirma."""


class TapoConnectionError(TapoPlugError):
    """Cihaza ulasilamadi veya komut basarisiz."""
