"""Pacote customizer para montagem e renderização de personagens."""
from .customizer import Character, Customizer, parts_catalog, load_catalog_from_assets


def __getattr__(name: str):
    if name == "CharacterRenderer":
        from .renderer import CharacterRenderer
        return CharacterRenderer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Character",
    "Customizer",
    "CharacterRenderer",
    "parts_catalog",
    "load_catalog_from_assets",
]