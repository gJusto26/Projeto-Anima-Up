"""Módulo de customização de personagens (recompensa pós-exercício).
Responsável pela montagem e sorteio de peças visuais dos personagens a partir
de um catálogo de assets segmentados em 3 partes principais:
- 'head' (cabeça)
- 'torso' (tronco com braços integrados)
- 'legs' (cintura para baixo em asset único)
Permite sorteio 100% livre (sem gênero) ou opcionalmente filtrado por tags
de gênero presentes no nome do arquivo (_M_, _F_, _U_).
"""
from __future__ import annotations

import random

class Character:
    """Representa a composição final de um personagem customizado.
    Attributes:
        parts (dict[str, str]): Mapeamento da categoria para o nome do arquivo
            (ex: {'head': 'cabeca_01.png', 'torso': 'tronco_01.png'})
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


heads = [
    "head_M_01.png",
    "head_M_02.png",
    "head_F_01.png",
    "head_F_02.png",
    "head_U_01.png",
]

torsos = [
    "torso_M_01.png",
    "torso_M_02.png",
    "torso_F_01.png",
    "torso_F_02.png",
    "torso_U_01.png"
]

legs = [
    "leg_M_01.png",
    "leg_M_02.png",
    "leg_F_01.png",
    "leg_F_02.png",
    "leg_U_01.png"
]

parts_catalog = {
    "head": heads,
    "torso": torsos,
    "leg": legs
}


if __name__ == "__main__":
    motor = Customizer(parts_catalog)

    #Modo sem gênero
    p_livre = motor.generate_random()
    print(f"Sem genero: {p_livre}")

    #Modo com gênero
    p_masculino = motor.generate_random(gender="M")
    print(f"Masculino: {p_masculino}")
