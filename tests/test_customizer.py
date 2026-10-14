"""Testes automatizados para o módulo de customização de personagens."""
import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no caminho de busca de módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from customizer import Customizer, Character, load_catalog_from_assets

# Catálogo mockado para garantir um ambiente controlado de testes:
MOCK_CATALOG = {
    "head": [
        "cabeca_M_01.png",
        "cabeca_F_01.png",
        "cabeca_U_01.png"
    ],
    "upper": [
        "tronco_M_01.png",
        "tronco_F_01.png",
        "tronco_U_01.png"
    ],
    "lower": [
        "perna_M_01.png",
        "perna_F_01.png",
        "perna_U_01.png"
    ]
}


def test_generate_random_without_gender():
    """Garante que a geração neutra sorteia todas as 3 categorias e não define gênero."""
    motor = Customizer(MOCK_CATALOG)
    character = motor.generate_random()

    assert isinstance(character, Character)
    assert character.gender is None
    assert "head" in character.parts
    assert "upper" in character.parts
    assert "lower" in character.parts


def test_generate_random_male_does_not_contain_female_assets():
    """Garante que um personagem 'M' nunca receba peças com a tag '_F_'."""
    motor = Customizer(MOCK_CATALOG)
    for _ in range(20):
        character = motor.generate_random(gender="M")
        assert character.gender == "M"
        for category, asset in character.parts.items():
            assert "_F_" not in asset, f"Peça feminina '{asset}' sorteada indevidamente para gênero 'M'!"


def test_generate_random_female_does_not_contain_male_assets():
    """Garante que um personagem 'F' nunca receba peças com a tag '_M_'."""
    motor = Customizer(MOCK_CATALOG)
    for _ in range(20):
        character = motor.generate_random(gender="F")
        assert character.gender == "F"
        for category, asset in character.parts.items():
            assert "_M_" not in asset, f"Peça masculina '{asset}' sorteada indevidamente para gênero 'F'!"


def test_invalid_gender_raises_value_error():
    """Garante que gêneros não suportados levantem uma exceção ValueError."""
    motor = Customizer(MOCK_CATALOG)
    try:
        motor.generate_random(gender="INVALIDO")
        assert False, "Deveria ter lançado ValueError para gênero inválido!"
    except ValueError:
        pass  # Comportamento esperado!


def test_empty_category_raises_value_error():
    """Garante que um catálogo incompleto/vazio lance erro informando o problema."""
    empty_catalog = {"head": [], "upper": ["tronco_01.png"]}
    motor = Customizer(empty_catalog)
    try:
        motor.generate_random()
        assert False, "Deveria ter lançado ValueError para categoria vazia!"
    except ValueError:
        pass  # Comportamento esperado!


def test_load_catalog_from_assets():
    """Garante que a descoberta automática carrega as categorias reais com sucesso."""
    catalog = load_catalog_from_assets()
    assert "head" in catalog
    assert "upper" in catalog
    assert "lower" in catalog
    assert len(catalog["head"]) >= 6
    assert len(catalog["upper"]) >= 6
    assert len(catalog["lower"]) >= 6


if __name__ == "__main__":
    test_generate_random_without_gender()
    test_generate_random_male_does_not_contain_female_assets()
    test_generate_random_female_does_not_contain_male_assets()
    test_invalid_gender_raises_value_error()
    test_empty_category_raises_value_error()
    test_load_catalog_from_assets()
    print("[OK] Todos os 6 testes do customizer passaram com sucesso!")
