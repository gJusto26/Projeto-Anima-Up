"""Módulo de customização de personagens (recompensa pós-exercício).
Responsável pela montagem e sorteio de peças visuais dos personagens a partir
de um catálogo de assets segmentados em 3 partes principais:
- 'head' (cabeça)
- 'upper' (tronco com braços integrados)
- 'lower' (cintura para baixo em asset único)
Permite sorteio 100% livre (sem gênero) ou opcionalmente filtrado por tags
de gênero presentes no nome do arquivo (_M_, _F_, _U_).
"""
from __future__ import annotations

import random

from pathlib import Path

class Character:
    """Representa a composição final de um personagem customizado.
    Attributes:
        parts (dict[str, str]): Mapeamento da categoria para o nome do arquivo
            (ex: {'head': 'head_alien.png', 'upper': 'upper_alien.png', 'lower': 'lower_alien.png'})
        gender (str | None): Gênero aplicado na geração ('M', 'F', 'U' ou None se for livre).
    """

    def __init__(self, parts: dict[str, str], gender: str | None = None) -> None:
        self.gender = gender
        self.parts = parts

    def __repr__(self) -> str:
        if self.gender:
            return f"<Character gender='{self.gender}' parts={self.parts}>"
        return f"<Character parts={self.parts}>"

class Customizer:
    """Motor de geração e customização de personagens.
    Gerencia o catálogo de partes disponíveis e realiza sorteios aleatórios,
    com suporte opcional a filtros por gênero.
    """
    def __init__(self, catalog: dict[str, list[str]]) -> None:
        """Inicializa o customizador com um catálogo de partes.
        Args:
            catalog: Dicionário onde a chave é a categoria (ex: 'head')
            e o valor é uma lista de nomes de arquivos disponíveis.
        """
        self.catalog = catalog

    def filter_parts(self, items: list[str], gender: str) -> list[str]:
        """Filtra uma lista de itens com base na tag de gênero do arquivo.
        Regras de compatibilidade:
            - 'M': aceita itens com '_M_' ou '_U_'.
            - 'F': aceita itens com '_F_' ou '_U_'.
            - 'U': aceita itens com '_M_', '_F_' ou '_U_'.
        Args:
            items: Lista de nomes de arquivos a serem filtrados.
            gender: Gênero desejado ('M', 'F' ou 'U').
        Returns:
            Lista contendo apenas os nomes de arquivo compatíveis.
        Raises:
            ValueError: Se o gênero informado não for 'M', 'F' ou 'U'.
        """
        filtered_parts = []
        if gender == "M":
            allowed_tags = ["M", "U"]
        elif gender == "F":
            allowed_tags = ["F", "U"]
        elif gender == "U":
            allowed_tags = ["M", "F", "U"]
        else:
            raise ValueError(f"Gênero '{gender}' inválido. Use 'M', 'F' ou 'U'.")

        for item in items:
            if any(f"_{tag}_" in item for tag in allowed_tags):
                filtered_parts.append(item)

        return filtered_parts
    
    def generate_random(self, gender: str | None = None) -> Character:
        """Gera um personagem aleatório selecionando uma peça de cada categoria.
        Se nenhum gênero for especificado, o sorteio é realizado sobre todo
        o catálogo da categoria de forma neutra/livre.
        Args:
            gender: Gênero opcional ('M', 'F', 'U' ou None para sorteio livre).
        Returns:
            Uma nova instância de Character com as peças sorteadas.
        Raises:
            ValueError: Se uma categoria do catálogo estiver vazia ou sem peças
                compatíveis com o gênero solicitado.
        """
        selected_parts = {}
        for category, item_list in self.catalog.items():
            if gender:
                options = self.filter_parts(item_list, gender)
            else:
                options = item_list

            if not options:
                raise ValueError(f"Nenhuma parte disponível na categoria '{category}'.")
            selected_parts[category] = random.choice(options)

        return Character(selected_parts, gender=gender)


def load_catalog_from_assets(assets_dir: str | Path = "assets") -> dict[str, list[str]]:
    """Varre automaticamente as subpastas de assets e monta o catálogo de peças.

    Args:
        assets_dir: Caminho base onde estão as pastas 'head', 'upper' e 'lower'.

    Returns:
        Dicionário com as categorias e suas respectivas listas de arquivos PNG encontrados.
    """
    base = Path(assets_dir)
    if not base.is_absolute() and not base.exists():
        project_root = Path(__file__).resolve().parent.parent
        candidate = project_root / assets_dir
        if candidate.exists():
            base = candidate

    return {
        "head": sorted([f.name for f in (base / "head").glob("*.png")]),
        "upper": sorted([f.name for f in (base / "upper").glob("*.png")]),
        "lower": sorted([f.name for f in (base / "lower").glob("*.png")]),
    }


parts_catalog = load_catalog_from_assets()


if __name__ == "__main__":
    motor = Customizer(parts_catalog)

    print("\n--- TESTE DO CUSTOMIZADOR COM ASSETS REAIS ---")
    p_livre = motor.generate_random()
    print(f"Personagem sorteado: {p_livre}")

