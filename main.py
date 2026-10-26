"""Ponto de entrada principal para teste e execução do Customizer."""
from customizer import CharacterRenderer, Customizer, parts_catalog


def main() -> None:
    print("=" * 50)
    print("   PROJETO ANIMA UP - SISTEMA DE CUSTOMIZAÇÃO")
    print("=" * 50)

    # 1. Inicializa o motor com o catálogo descoberto automaticamente
    customizer = Customizer(parts_catalog)
    print("\n[1] Catálogo de peças carregado:")
    for category, items in parts_catalog.items():
        print(f"    - {category}: {len(items)} peças encontradas")

    # 2. Sorteia um personagem aleatório
    personagem = customizer.generate_random()
    print("\n[2] Personagem sorteado com sucesso:")
    for category, asset in personagem.parts.items():
        print(f"    - {category}: {asset}")

    # 3. Renderiza e sobrepõe as camadas em imagem final
    renderer = CharacterRenderer("assets")
    output_file = "character_teste.png"
    caminho = renderer.save_to_file(personagem, output_file)
    print(f"\n[3] Imagem renderizada e salva em:")
    print(f"    -> {caminho.resolve()}")
    print("\n[OK] Concluído com sucesso!\n")


if __name__ == "__main__":
    main()

