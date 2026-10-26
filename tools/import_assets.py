"""Script utilitário para importação, processamento de Chroma Key e organização de assets.

Lê imagens brutas (com fundo verde), remove o verde tornando-o 100% transparente
e distribui os arquivos automaticamente nas pastas oficiais:
- assets/head/
- assets/upper/
- assets/lower/
- assets/fx/
"""
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"


def remove_chroma_key(
    image: Image.Image,
    t_low: int = 10,
    t_high: int = 35,
) -> Image.Image:
    """Remove o fundo verde (Chroma Key) e o vazamento de verde (Despill) nas bordas.

    Utiliza o método de diferença linear de cores com supressão de spill:
    1. diff = G - max(R, B): mede o quanto o canal verde domina a cor do pixel.
    2. diff >= t_high: fundo verde puro/dominante -> 100% transparente (Alpha = 0).
    3. t_low < diff < t_high: transição suave na borda -> ajusta Alpha proporcional e neutraliza o verde.
    4. diff > 0: borda ou contorno -> aplica Despill (limita G a max(R, B)), eliminando qualquer halo verde.

    Args:
        image: Imagem original do Pillow.
        t_low: Limite inferior da dominância do verde para início da suavização.
        t_high: Limite superior onde o verde é considerado 100% fundo.

    Returns:
        Image.Image convertida em RGBA com fundo transparente e bordas limpas sem verde.
    """
    image = image.convert("RGBA")
    raw = bytearray(image.tobytes())

    # Percorre os pixels em blocos de 4 bytes (R, G, B, A)
    for i in range(0, len(raw), 4):
        r, g, b, a = raw[i], raw[i + 1], raw[i + 2], raw[i + 3]
        if a == 0:
            continue

        max_rb = r if r > b else b
        diff = g - max_rb

        if diff >= t_high:
            raw[i + 3] = 0  # 100% transparente
        elif diff > t_low:
            # Transição suave para evitar serrilhado
            factor = (t_high - diff) / (t_high - t_low)
            raw[i + 3] = int(a * factor)
            raw[i + 1] = max_rb  # Despill (remove a contaminação verde)
        elif diff > 0:
            # Despill para qualquer tom residual de verde nas bordas
            raw[i + 1] = max_rb

    return Image.frombytes("RGBA", image.size, bytes(raw))


def process_and_route_assets(source_folder: Path) -> None:
    """Processa todas as imagens de uma pasta de origem e organiza nas pastas oficiais."""
    if not source_folder.exists():
        print(f"[ERRO] Pasta de origem não encontrada: {source_folder}")
        return

    png_files = sorted(source_folder.glob("*.png"))
    if not png_files:
        print(f"[AVISO] Nenhum arquivo .png encontrado em: {source_folder}")
        return

    print(f"\n--- Iniciando processamento de {len(png_files)} assets de '{source_folder.name}' ---")

    count = 0
    for file_path in png_files:
        filename = file_path.name.lower()

        # Identifica a categoria pelo prefixo
        if filename.startswith("head_"):
            target_dir = ASSETS_DIR / "head"
        elif filename.startswith("upper_"):
            target_dir = ASSETS_DIR / "upper"
        elif filename.startswith("lower_"):
            target_dir = ASSETS_DIR / "lower"
        elif filename.startswith("fx_"):
            target_dir = ASSETS_DIR / "fx"
        else:
            print(f"  [PULADO] Categoria desconhecida: {file_path.name}")
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        dest_path = target_dir / file_path.name

        # Processa e salva com transparência
        with Image.open(file_path) as img:
            transparent_img = remove_chroma_key(img)
            transparent_img.save(dest_path, format="PNG")

        print(f"  [OK] {file_path.name} -> {target_dir.name}/{file_path.name}")
        count += 1

    print(f"\n[SUCESSO] {count} arquivos processados e organizados com fundo transparente!\n")


if __name__ == "__main__":
    # 1. Tenta a pasta específica 'drive_images'
    drive_folder = ASSETS_DIR / "drive_images"
    if drive_folder.exists():
        process_and_route_assets(drive_folder)
    else:
        # 2. Busca qualquer pasta com padrão 'drive*'
        matching_folders = list(ASSETS_DIR.glob("drive*"))
        if matching_folders:
            for folder in matching_folders:
                process_and_route_assets(folder)
        else:
            # 3. Fallback para pasta 'raw'
            raw_folder = ASSETS_DIR / "raw"
            process_and_route_assets(raw_folder)

