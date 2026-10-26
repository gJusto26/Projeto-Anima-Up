"""Testes automatizados para o módulo de renderização gráfica (CharacterRenderer)."""
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Garante que a raiz do projeto esteja no caminho de busca de módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from customizer import Character, CharacterRenderer


def test_layer_order():
    """Garante que a ordem de camadas respeite lower -> upper -> head."""
    assert CharacterRenderer.LAYER_ORDER == ("lower", "upper", "head")


def test_render_with_mock_images():
    """Garante que o renderer sobrepõe as imagens RGBA e gera o resultado esperado."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        (base_dir / "head").mkdir()
        (base_dir / "upper").mkdir()
        (base_dir / "lower").mkdir()

        # Cria imagens de teste de 50x50 pixels
        img_head = Image.new("RGBA", (50, 50), (255, 0, 0, 255))
        img_upper = Image.new("RGBA", (50, 50), (0, 255, 0, 255))
        img_lower = Image.new("RGBA", (50, 50), (0, 0, 255, 255))

        img_head.save(base_dir / "head" / "head_1.png")
        img_upper.save(base_dir / "upper" / "upper_1.png")
        img_lower.save(base_dir / "lower" / "lower_1.png")

        character = Character({
            "head": "head_1.png",
            "upper": "upper_1.png",
            "lower": "lower_1.png",
        })

        renderer = CharacterRenderer(assets_dir=base_dir)
        result = renderer.render(character)

        assert isinstance(result, Image.Image)
        assert result.size == (50, 50)
        assert result.mode == "RGBA"

        # Testa também o salvamento em disco
        out_path = base_dir / "output.png"
        saved = renderer.save_to_file(character, out_path)
        assert saved.exists()
        assert saved.stat().st_size > 0


def test_render_missing_asset_raises_filenotfound():
    """Garante que FileNotFoundError é lançado se o arquivo de asset não existir."""
    renderer = CharacterRenderer(assets_dir="caminho_inexistente_12345")
    character = Character({"head": "nao_existe.png"})

    try:
        renderer.render(character)
        assert False, "Deveria ter lançado FileNotFoundError!"
    except FileNotFoundError:
        pass


def test_render_empty_character_raises_value_error():
    """Garante que ValueError é lançado ao tentar renderizar personagem sem partes."""
    renderer = CharacterRenderer()
    character = Character({})

    try:
        renderer.render(character)
        assert False, "Deveria ter lançado ValueError!"
    except ValueError:
        pass


def test_render_cv2_defense():
    """Garante que render_cv2 lança ImportError claro se dependências não estiverem instaladas."""
    renderer = CharacterRenderer()
    character = Character({"head": "qualquer.png"})
    try:
        import cv2
        import numpy as np
        has_deps = True
    except ImportError:
        has_deps = False

    if not has_deps:
        try:
            renderer.render_cv2(character)
            assert False, "Deveria ter lançado ImportError para falta de cv2/numpy!"
        except ImportError as e:
            assert "opencv-python" in str(e)


if __name__ == "__main__":
    test_layer_order()
    test_render_with_mock_images()
    test_render_missing_asset_raises_filenotfound()
    test_render_empty_character_raises_value_error()
    test_render_cv2_defense()
    print("[OK] Todos os testes do renderer passaram com sucesso!")

