"""Testes automatizados para o algoritmo de Chroma Key e Despill."""
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.import_assets import remove_chroma_key


def test_remove_pure_green():
    """Garante que verde puro (#00FF00) fica 100% transparente."""
    img = Image.new("RGBA", (10, 10), (0, 255, 0, 255))
    result = remove_chroma_key(img)
    for y in range(10):
        for x in range(10):
            assert result.getpixel((x, y))[3] == 0, "Pixel verde deveria estar transparente!"


def test_remove_antialiased_dark_green():
    """Garante que verdes escuros das bordas suavizadas também são eliminados."""
    # Pixel que antes sobrava com g <= 150
    img = Image.new("RGBA", (1, 1), (0, 100, 0, 255))
    result = remove_chroma_key(img)
    assert result.getpixel((0, 0))[3] == 0, "Verde escuro de borda deveria ser transparente!"


def test_despill_residual_green():
    """Garante que pixels de contorno com vazamento de verde são descontaminados (despilled)."""
    # Exemplo: contorno preto levemente esverdeado (10, 30, 10)
    img = Image.new("RGBA", (1, 1), (10, 30, 10, 255))
    result = remove_chroma_key(img)
    r, g, b, a = result.getpixel((0, 0))
    # O verde (g) deve ter sido reduzido ao máximo entre R e B
    assert g <= max(r, b), f"Despill falhou: pixel ainda está esverdeado ({r}, {g}, {b})!"


def test_preserve_non_green_colors():
    """Garante que cores legítimas do personagem (branco, preto, vermelho, etc.) são preservadas."""
    img = Image.new("RGBA", (2, 2))
    img.putpixel((0, 0), (255, 0, 0, 255))      # Vermelho
    img.putpixel((1, 0), (255, 255, 255, 255))  # Branco
    img.putpixel((0, 1), (0, 0, 0, 255))        # Preto
    img.putpixel((1, 1), (80, 50, 20, 255))     # Marrom

    result = remove_chroma_key(img)
    assert result.getpixel((0, 0)) == (255, 0, 0, 255)
    assert result.getpixel((1, 0)) == (255, 255, 255, 255)
    assert result.getpixel((0, 1)) == (0, 0, 0, 255)
    assert result.getpixel((1, 1)) == (80, 50, 20, 255)


if __name__ == "__main__":
    test_remove_pure_green()
    test_remove_antialiased_dark_green()
    test_despill_residual_green()
    test_preserve_non_green_colors()
    print("[OK] Todos os testes de Chroma Key e Despill passaram com sucesso!")

