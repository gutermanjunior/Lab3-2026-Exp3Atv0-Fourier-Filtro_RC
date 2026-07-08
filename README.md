# 📡 Onda Quadrada, Fourier e Filtro RC Passa-Baixa

### **Instituto de Física da Universidade de São Paulo (IFUSP)**

#### *Experimento 3 - Atividade 0 | Disciplina: 4302213 - Física Experimental III*

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/plotting-Matplotlib-orange.svg?style=for-the-badge)](https://matplotlib.org/)
[![NumPy](https://img.shields.io/badge/numerical-NumPy-4D77CF.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![IFUSP](https://img.shields.io/badge/institution-IFUSP-red.svg?style=for-the-badge)](https://portal.if.usp.br/ifusp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

> 📘 **Sobre este repositório:**  
> Este projeto reúne material didático em Python para visualizar a decomposição de uma onda quadrada em harmônicos de Fourier e estudar qualitativamente como um filtro RC passa-baixa modifica essa onda no domínio do tempo.
>
> ⚠️ **Status atual:** este repositório está em desenvolvimento inicial. O programa ainda não está em sua forma final e pode conter partes incompletas, ajustes pendentes ou mudanças futuras de interface e organização.

---

## 🧾 TL;DR

Programa didático e interativo em Python para mostrar que uma onda quadrada pode ser aproximada pela soma de harmônicos ímpares de Fourier e que um filtro RC passa-baixa atenua principalmente os harmônicos de maior frequência.

A ideia central é:

```text
onda quadrada
    → harmônicos ímpares de Fourier
    → ganho passa-baixa G(f)
    → atenuação de cada harmônico
    → reconstrução da onda filtrada
```

---

## ⚠️ Comece por aqui

Este repositório foi criado para apoiar uma atividade didática de **Física Experimental III - Lab3**, conectando simulação computacional, análise de Fourier e observações feitas em bancada com circuito RC.

O programa principal deverá permitir:

1. escolher o número `N` de harmônicos ímpares da onda quadrada;
2. definir a frequência fundamental da onda quadrada;
3. definir um ganho passa-baixa aproximado por duas retas;
4. calcular a frequência de cada harmônico;
5. multiplicar cada harmônico pelo ganho do filtro na frequência correspondente;
6. comparar a onda quadrada original com a onda filtrada.

---

## 📋 Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Contexto Didático](#contexto-didatico)
3. [Fundamentação Teórica](#fundamentacao-teorica)
4. [Fluxo Conceitual](#fluxo-conceitual)
5. [Funcionalidades Previstas](#funcionalidades-previstas)
6. [Estado Atual do Projeto](#estado-atual-do-projeto)
7. [Estrutura do Repositório](#estrutura-do-repositorio)
8. [Como Usar](#como-usar)
9. [Uso Didático Esperado](#uso-didatico-esperado)
10. [Resultado Esperado](#resultado-esperado)
11. [Próximos Passos](#proximos-passos)
12. [Como Citar](#como-citar)
13. [Créditos e Instituição](#creditos-e-instituicao)

---

<a id="sobre-o-projeto"></a>

## 📖 Sobre o Projeto

Este projeto tem como objetivo construir uma ferramenta didática em Python para explorar a relação entre:

* séries de Fourier;
* ondas quadradas;
* harmônicos ímpares;
* resposta em frequência;
* filtros passa-baixa;
* circuitos RC;
* comparação qualitativa entre simulação e bancada.

A proposta é permitir que estudantes visualizem, de forma interativa, como uma onda quadrada é composta por harmônicos de diferentes frequências e como um circuito RC passa-baixa atenua esses harmônicos de maneira seletiva.

O foco não é apenas gerar gráficos, mas ajudar o estudante a entender a ponte entre o domínio do tempo e o domínio da frequência.

---

<a id="contexto-didatico"></a>

## 📌 Contexto Didático

Em uma onda quadrada ideal, a forma abrupta das transições está associada à presença de harmônicos de alta frequência. Quando essa onda passa por um filtro passa-baixa, os harmônicos mais altos são atenuados mais intensamente.

Como consequência, a onda filtrada tende a apresentar:

* transições menos abruptas;
* redução das oscilações rápidas;
* aparência mais suave;
* menor semelhança com a onda quadrada ideal quando o corte do filtro é baixo;
* maior semelhança com a onda quadrada ideal quando mais harmônicos passam com ganho próximo de 1.

A atividade permite conectar diretamente três observações:

1. a composição harmônica da onda quadrada;
2. o gráfico de ganho em função da frequência medido ou estimado para o filtro RC;
3. a forma de onda observada no osciloscópio.

---

<a id="fundamentacao-teorica"></a>

## ⚛️ Fundamentação Teórica

### Série de Fourier da onda quadrada

Uma onda quadrada ímpar, de amplitude normalizada entre aproximadamente `-1` e `+1`, pode ser escrita como:

$$
v_{\text{in}}(t)
=
\frac{4}{\pi}
\sum_{k=1}^{N}
\frac{
\sin\left[2\pi(2k-1)f_0t\right]
}{
2k-1
}.
$$

Aqui:

* `N` é o número de harmônicos ímpares incluídos;
* `f0` é a frequência fundamental da onda quadrada;
* o termo `2k - 1` seleciona apenas os harmônicos ímpares;
* os harmônicos presentes são `f0`, `3f0`, `5f0`, `7f0`, etc.

Portanto, a frequência do harmônico de índice `k` é:

$$
f_k = (2k-1)f_0.
$$

---

### Ganho passa-baixa

Um filtro passa-baixa preserva melhor as componentes de baixa frequência e atenua as componentes de alta frequência.

Neste projeto, o ganho do filtro é representado por uma função:

$$
G(f)
$$

com valores tipicamente entre `0` e `1`.

O efeito do filtro sobre cada harmônico é modelado como:

$$
A_{k,\text{filtrado}}
=
A_k G(f_k).
$$

Assim, a onda filtrada pode ser reconstruída por:

$$
v_{\text{out}}(t)
=
\frac{4}{\pi}
\sum_{k=1}^{N}
G(f_k)
\frac{
\sin\left[2\pi(2k-1)f_0t\right]
}{
2k-1
}.
$$

---

### Observação sobre fase

Na forma inicial do programa, a filtragem pode ser tratada apenas como atenuação de amplitude.

Isso é suficiente para uma primeira visualização qualitativa, mas não descreve completamente a resposta real de um circuito RC, pois o filtro também introduz defasagem dependente da frequência.

Para um filtro RC passa-baixa ideal medido sobre o capacitor:

$$
H(f)
=
\frac{1}{1+jf/f_c},
$$

com módulo:

$$
|H(f)|
=
\frac{1}{\sqrt{1+(f/f_c)^2}},
$$

e fase:

$$
\phi(f)
=
-\arctan(f/f_c).
$$

Uma versão posterior do programa poderá incluir essa fase para melhorar a comparação com sinais medidos em bancada.

---

<a id="fluxo-conceitual"></a>

## 🛠️ Fluxo Conceitual

```mermaid
flowchart LR

A[Onda quadrada no tempo] --> B[Série de Fourier]
B --> C[Harmônicos ímpares: f0, 3f0, 5f0...]
C --> D[Ganho passa-baixa G(f)]
D --> E[Multiplicação A_k por G(f_k)]
E --> F[Reconstrução da onda filtrada]
F --> G[Comparação qualitativa com a bancada]

style A fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
style B fill:#ede7f6,stroke:#5e35b1,stroke-width:1px
style C fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
style D fill:#d9f2d9,stroke:#2e7d32,stroke-width:1px
style E fill:#fce4ec,stroke:#c2185b,stroke-width:1px
style F fill:#e0f7fa,stroke:#00838f,stroke-width:1px
style G fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px
```

---

<a id="funcionalidades-previstas"></a>

## 💻 Funcionalidades Previstas

O programa deverá incluir:

* visualização da onda quadrada ideal;
* soma parcial de Fourier com `N` harmônicos ímpares;
* controle interativo do número de harmônicos por `Slider`;
* cálculo automático das frequências dos harmônicos;
* aplicação de um ganho passa-baixa a cada harmônico;
* comparação entre a onda antes e depois do filtro;
* gráfico do ganho em função da frequência;
* indicação dos harmônicos usados sobre o gráfico de ganho;
* visualização das amplitudes harmônicas antes e depois da filtragem;
* opção para mostrar ou ocultar harmônicos individuais.

Funcionalidades futuras podem incluir:

* entrada de dados experimentais por arquivo `.csv`;
* interpolação do ganho medido em bancada;
* comparação entre ganho experimental e ganho teórico RC;
* inclusão da fase do filtro RC;
* exportação automática de figuras;
* versão em notebook para uso no Google Colab;
* versão em script `.py` para execução local.

---

<a id="estado-atual-do-projeto"></a>

## 🚧 Estado Atual do Projeto

Este repositório está em fase inicial.

O programa ainda pode passar por mudanças importantes em:

* nome dos arquivos;
* organização das funções;
* interface gráfica;
* entrada de parâmetros;
* modelo de ganho passa-baixa;
* inclusão ou não de fase;
* estrutura das pastas;
* documentação para alunos.

Neste primeiro commit, o objetivo é registrar publicamente a proposta, iniciar a organização do repositório e estabelecer uma base de desenvolvimento didático.

---

<a id="estrutura-do-repositorio"></a>

## 📁 Estrutura do Repositório

Estrutura inicial sugerida:

```bash
├── README.md                                   # Documentação principal do projeto
├── LICENSE                                     # Licença do código-fonte
├── .gitignore                                  # Arquivos ignorados pelo Git
├── fourier_onda_quadrada_filtro_rc.py           # Programa principal em desenvolvimento
├── figures/                                    # Figuras exportadas ou usadas na documentação
├── data/                                       # Dados de exemplo ou dados experimentais futuros
│   ├── examples/                               # Arquivos pequenos de exemplo
│   └── raw/                                    # Dados brutos locais, preferencialmente não versionados
└── docs/                                       # Materiais didáticos complementares
```

A estrutura poderá ser modificada conforme o projeto amadurecer.

---

<a id="como-usar"></a>

## 🚀 Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC.git
```

Entre na pasta:

```bash
cd Lab3-2026-Exp3Atv0-Fourier-Filtro_RC
```

---

### 2. Crie um ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install numpy matplotlib
```

---

### 4. Execute o programa

```bash
python fourier_onda_quadrada_filtro_rc.py
```

---

<a id="uso-didatico-esperado"></a>

## 🧪 Uso Didático Esperado

Durante a atividade, o estudante deverá observar que:

1. com poucos harmônicos, a onda quadrada é mal aproximada;
2. ao aumentar `N`, a aproximação melhora, mas aparecem oscilações próximas às descontinuidades;
3. harmônicos de ordem mais alta são importantes para tornar as bordas da onda mais abruptas;
4. o filtro passa-baixa reduz principalmente esses harmônicos de alta frequência;
5. a onda filtrada fica mais suave;
6. a forma da onda filtrada depende da relação entre a frequência fundamental da onda quadrada, seus harmônicos e a frequência de corte do filtro.

---

<a id="resultado-esperado"></a>

## 📊 Resultado Esperado

A interface final deverá mostrar, em uma única janela:

1. a onda quadrada ideal;
2. a soma de Fourier antes do filtro;
3. a soma de Fourier após o filtro;
4. o ganho passa-baixa em função da frequência;
5. os pontos correspondentes aos harmônicos usados;
6. as amplitudes dos harmônicos antes e depois da filtragem.

A comparação qualitativa esperada é:

```text
mais harmônicos preservados pelo filtro
    → onda filtrada mais parecida com a onda quadrada

harmônicos altos fortemente atenuados
    → onda filtrada mais arredondada e suave
```

---

<a id="proximos-passos"></a>

## 🧭 Próximos Passos

Tarefas planejadas para versões futuras:

* [ ] estabilizar o script principal;
* [ ] revisar a interface gráfica;
* [ ] separar funções matemáticas de funções de visualização;
* [ ] adicionar entrada de dados experimentais por CSV;
* [ ] permitir interpolação do ganho medido pelos alunos;
* [ ] adicionar opção para incluir fase do filtro RC;
* [ ] exportar figuras automaticamente;
* [ ] criar exemplos de uso com diferentes frequências fundamentais;
* [ ] criar um roteiro curto para os alunos;
* [ ] adicionar imagens demonstrativas ao README;
* [ ] criar `requirements.txt`;
* [ ] criar `CITATION.cff`.

---

<a id="como-citar"></a>

## 📜 Como Citar

Se este código for útil para seu relatório, aula, monitoria ou material didático, cite este repositório:

> **Araujo Junior, G. R.** (2026). *Onda Quadrada, Fourier e Filtro RC Passa-Baixa: Exp3Atv0*. GitHub Repository.  
> `https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC`

Quando o arquivo `CITATION.cff` estiver disponível, dê preferência à citação indicada nele.

---

<a id="creditos-e-instituicao"></a>

## 👨‍🔬 Créditos e Instituição

* **Desenvolvedor:** Guterman Rodrigues de Araujo Junior
* **Vínculo:** Mestrado em Física - IFUSP
* **Disciplina:** 4302213 - Física Experimental III
* **Atividade:** Experimento 3 - Atividade 0
* **Local:** Instituto de Física da Universidade de São Paulo (IFUSP)

---

<div align="center">
  <sub>Material didático em desenvolvimento para apoio à Física Experimental III - IFUSP.</sub>
</div>