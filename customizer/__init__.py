"""Pacote customizer para montagem e renderização de personagens."""
from .customizer import Character, Customizer, parts_catalog, load_catalog_from_assets
from .renderer import CharacterRenderer

__all__ = [
    "Character",
    "Customizer",
    "CharacterRenderer",
    "parts_catalog",
    "load_catalog_from_assets",
]