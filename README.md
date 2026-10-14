# Projeto Anima Up - Módulo de Customização (Customizer)

Módulo em Python responsável pela customização, sorteio e renderização visual em camadas (composição gráfica com Pillow) de personagens para o projeto **Anima Up / Squat-Totem** (sistema de recompensas pós-exercício).

---

## 📁 Estrutura do Projeto

```text
Projeto Anima Up/
├── assets/
│   ├── drive_images/       # Imagens brutas recebidas (com chroma key verde)
│   ├── head/               # Assets da cabeça (camada 1 - fundo)
│   ├── upper/              # Tronco com braços integrados (camada 2 - meio)
│   ├── lower/              # Cintura para baixo: quadril/pernas/pés (camada 3 - frente)
│   └── fx/                 # Efeitos visuais e auras (opcional)
├── customizer/
│   ├── __init__.py         # Exportação pública do pacote
│   ├── customizer.py       # Lógica de seleção aleatória e filtro de gênero
│   └── renderer.py         # Renderização gráfica e sobreposição (Pillow RGBA)
├── tests/
│   ├── test_customizer.py  # Testes unitários do motor de sorteio
│   ├── test_renderer.py    # Testes unitários do renderizador Pillow
│   └── run_all.py          # Script para execução unificada da suíte de testes
├── tools/
│   └── import_assets.py    # Utilitário para remoção de chroma key e roteamento de assets
├── requirements.txt
└── README.md
```

---

## 🎨 Ordem de Camadas (Layer Ordering)

O renderizador sobrepõe as peças utilizando composição Alpha RGBA na seguinte ordem estrita:
1. **`head`** (Cabeça / Elmos / Cabelos) — Camada base (fundo)
2. **`upper`** (Tronco com braços integrados) — Camada intermediária
3. **`lower`** (Cintura para baixo em peça única) — Camada superior (frontal)

---

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Gerar e Renderizar um Personagem
Para sortear peças automaticamente a partir das pastas de `assets/` e gerar uma imagem final (`character_teste.png`):
```bash
python -m customizer.renderer
```

### 3. Executar Testes Automatizados
Para rodar toda a suíte de testes unitários:
```bash
python tests/run_all.py
```

### 4. Importar Novos Assets com Remoção de Chroma Key
Coloque novos arquivos `.png` (com fundo verde) na pasta `assets/drive_images/` e execute:
```bash
python tools/import_assets.py
```
O script removerá o verde automaticamente (deixando o fundo 100% transparente) e distribuirá os arquivos nas respectivas pastas (`assets/head/`, `assets/upper/`, `assets/lower/`, `assets/fx/`).
