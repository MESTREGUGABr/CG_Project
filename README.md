# 🗿 CG Project — 3D Statue Viewer

Aplicação gráfica 3D desenvolvida em **Python + OpenGL** para a disciplina de Computação Gráfica. O projeto é um visualizador interativo de modelos 3D (estátuas) com sistema de iluminação dinâmica, câmera orbital e suporte a múltiplos modelos `.obj`.

---

## 📸 Visão Geral

O **3D Statue Viewer** permite carregar e visualizar modelos 3D no formato Wavefront OBJ, navegando ao redor deles com uma câmera orbital controlada pelo mouse. A aplicação conta com dois modos de iluminação — um sol orbital animado e múltiplos spotlights posicionáveis — e utiliza o modelo de iluminação **Blinn-Phong** implementado em GLSL.

---

## ✅ Requisitos do Projeto Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| **3D** | ✅ | Cena 3D com modelos `.obj`, câmera orbital, projeção perspectiva |
| **Interação (Mouse/Teclado)** | ✅ | Mouse: rotação e zoom da câmera. Teclado: troca de modelo, modos de luz, spotlights |
| **Estrutura de Dados** | ✅ | Classes organizadas: `Mesh`, `Scene`, `Camera`, `Light`, `Shader`, `Grid`, `InputHandler` |
| **(EXTRA) Sombreamento** | ✅ | Iluminação Blinn-Phong com luz direcional, spotlights e atenuação |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pygame** — janela, contexto OpenGL e captura de eventos
- **PyOpenGL** — bindings OpenGL para Python
- **NumPy** — operações com matrizes e vetores
- **GLSL 3.30 Core** — shaders de vértice e fragmento
- **Wavefront OBJ** — formato de modelos 3D

---

## 📁 Estrutura do Projeto

```
3d-statue-viewer/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
├── .gitignore
│
├── engine/                    # Motor gráfico
│   ├── camera.py              # Câmera orbital (yaw/pitch/zoom)
│   ├── grid.py                # Plano de chão com grid
│   ├── input_handler.py       # Captura de mouse e teclado
│   ├── light.py               # SunLight, SpotLight, SpotLightManager
│   ├── mesh.py                # Carregamento de .obj e buffers OpenGL
│   ├── scene.py               # Gerenciador de cena (modelos, luzes, câmera)
│   ├── shader.py              # Compilação e gerenciamento de shaders
│   └── transform.py           # Matrizes de transformação (model, view, projection)
│
├── shaders/                   # Shaders GLSL
│   ├── vertex.glsl            # Vertex shader (modelo 3D)
│   ├── fragment.glsl          # Fragment shader (iluminação Blinn-Phong)
│   ├── grid_vertex.glsl       # Vertex shader (grid do chão)
│   └── grid_fragment.glsl     # Fragment shader (padrão de grid)
│
└── models/                    # Modelos 3D (.obj) — não incluídos no repo
    ├── bunny.obj              # Exemplo: Stanford Bunny
    └── dragon.obj             # Exemplo: Stanford Dragon
```

---

## 🚀 Como Rodar

### 1. Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install pygame PyOpenGL numpy
```

### 3. Adicionar modelos 3D

Coloque arquivos `.obj` na pasta `models/`. A aplicação carrega automaticamente todos os `.obj` encontrados nessa pasta.

**Modelos sugeridos (gratuitos):**
- [Stanford Bunny](https://graphics.stanford.edu/data/3Dscanrep/)
- [Stanford Dragon](https://graphics.stanford.edu/data/3Dscanrep/)
- Qualquer modelo `.obj` exportado do Blender ou baixado de sites como [Sketchfab](https://sketchfab.com)

> **Nota:** Os modelos são automaticamente normalizados (centralizados na origem e escalados para caber em uma esfera unitária), então qualquer modelo `.obj` deve funcionar sem ajustes.

### 4. Executar

```bash
python main.py
```

---

## 🎮 Controles

| Entrada | Ação |
|---------|------|
| **Mouse (arrastar LMB)** | Rotacionar câmera ao redor do modelo |
| **Scroll do mouse** | Zoom in / Zoom out |
| **Tab** | Alternar entre modelos carregados |
| **1** | Modo Sol (luz direcional orbital animada) |
| **2** | Modo Spotlight |
| **Espaço** | Adicionar spotlight na posição atual da câmera |
| **C** | Limpar todos os spotlights |
| **+/-** | Aumentar/diminuir velocidade do sol |
| **ESC** | Sair |

---

## 🔧 Detalhes Técnicos

### Pipeline Gráfico
A aplicação utiliza **OpenGL 3.3 Core Profile** com o pipeline programável (shaders). O fluxo de renderização é:

1. **Vértices** → Vertex Shader (transformações Model → View → Projection)
2. **Fragmentos** → Fragment Shader (cálculo de iluminação Blinn-Phong)
3. **Framebuffer** → Tela

### Iluminação
- **Modelo Blinn-Phong**: componentes ambiente + difusa + especular
- **Luz direcional (Sol)**: orbita ao redor da cena com velocidade configurável
- **Spotlights**: até 9 spotlights com cone de iluminação, atenuação por distância e suavização nas bordas
- **Normal Matrix**: calculada como a inversa transposta da submatriz 3×3 do model matrix, garantindo transformação correta das normais

### Carregamento de Modelos
- Parser customizado de arquivos Wavefront OBJ (vértices, normais, faces)
- Fan triangulation para faces com mais de 3 vértices
- Cálculo automático de normais suaves (smooth normals) quando não presentes no arquivo
- Normalização automática para esfera unitária na origem

### Estruturas de Dados
- **VAO/VBO/EBO**: buffers OpenGL para geometria (vertex data interleaved: posição + normal)
- **Dicionário de uniforms**: cache de localizações de uniforms no shader
- **Lista de meshes**: múltiplos modelos carregáveis dinamicamente
- **Lista de spotlights**: gerenciador com limite de 9 spotlights

---

## 📝 Licença

Projeto acadêmico — uso educacional.
