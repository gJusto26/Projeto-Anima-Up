"""Módulo de renderização gráfica de personagens com Pillow.
Carrega os assets visuais do disco e sobrepõe as camadas na ordem definida:
1. 'lower' (cintura para baixo) - camada do fundo
2. 'upper' (tronco com braços) - camada intermediária
3. 'head' (cabeça) - camada superior/frontal
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

try:
    from .customizer import Character
except ImportError:
    from customizer import Character

class CharacterRenderer:
    """Responsável por carregar e sobrepor as partes visuais de um Character."""

    LAYER_ORDER = ("lower", "upper", "head")

    def __init__(self, assets_dir: str | Path = "assets") -> None:
        """Inicializa o renderizador apontando para a pasta raiz dos assets.
            Args:
            assets_dir: Caminho base onde estão as subpastas 'head', 'upper' e 'lower'.
        """
        self.assets_dir = Path(assets_dir)

    def get_part_path(self, category: str, filename: str) -> Path:
        """Retorna o caminho completo de um asset no disco.
        Args:
            category: Nome da categoria ('head', 'upper' ou 'lower').
            filename: Nome do arquivo (ex: 'head_alien.png').
        Returns:
        Path apontando para o arquivo no sistema de arquivos."""
        return self.assets_dir / category / filename

    def render(self, character: Character) -> Image.Image:
        """Renderiza o personagem combinando as peças na ordem de sobreposição correta.
        Args:
            character: Instância de Character contendo o dicionário parts.
        Returns:
            Image.Image transparente contendo o personagem montado.
        Raises:
            FileNotFoundError: Se algum arquivo de asset não for encontrado no disco.
            ValueError: Se o personagem não possuir peças para renderizar."""
        composite_image: Image.Image | None = None

        for category in self.LAYER_ORDER:
            filename = character.parts.get(category)
            if not filename:
                continue
            filepath = self.get_part_path(category, filename)
            if not filepath.exists():
                raise FileNotFoundError(f"Asset '{filename}' não encontrado em '{filepath}'.")
            part_image = Image.open(filepath).convert("RGBA")
            if composite_image is None:
                composite_image = part_image
            else:
                composite_image = Image.alpha_composite(composite_image, part_image)

        if composite_image is None:
            raise ValueError("O personagem não possui nenhuma parte válida para renderizar.")

        return composite_image

    def save_to_file(self, character: Character, output_path : str | Path) -> Path:
        """Renderiza o personagem e salva como arquivo PNG no disco.
        Args:
            character: Instância de Character.
            output_path: Caminho do arquivo de destino (ex: 'caracter_montado.png').
        Returns:
            Path do arquivo salvo."""
        image = self.render(character)
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        image.save(dest, format="PNG")
        return dest

if __name__ == "__main__":
    try:
        from .customizer import Customizer, parts_catalog
    except ImportError:
        from customizer.customizer import Customizer, parts_catalog
    motor = Customizer(parts_catalog)
    personagem = motor.generate_random()
    renderer = CharacterRenderer("assets")
    caminho = renderer.save_to_file(personagem, "character_teste.png")
    print(f"[OK] Personagem montado e salvo com sucesso em: {caminho}")