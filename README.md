# 📡 Onda Quadrada, Fourier e Filtro RC Passa-Baixa

### Instituto de Física da Universidade de São Paulo (IFUSP)

#### Experimento 3 — Atividade 0 | Disciplina 4302213 — Física Experimental III

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/numerical-NumPy-4D77CF.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/plotting-Matplotlib-orange.svg?style=for-the-badge)](https://matplotlib.org/)
[![IFUSP](https://img.shields.io/badge/institution-IFUSP-red.svg?style=for-the-badge)](https://portal.if.usp.br/ifusp/)
[![Status](https://img.shields.io/badge/status-protótipo%20didático-yellow.svg?style=for-the-badge)](#estado-atual)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## TL;DR

Este repositório contém um programa didático em Python para estudar, de forma interativa, como uma onda quadrada pode ser reconstruída por uma série de Fourier e como um filtro RC passa-baixa altera essa onda ao atenuar seus harmônicos.

A ideia central é:

```text
onda quadrada no tempo
    → decomposição em harmônicos ímpares
    → ganho passa-baixa em função da frequência
    → atenuação de cada harmônico
    → reconstrução temporal da onda após o filtro
```

A interface atual permite comparar:

- a onda quadrada ideal;
- a soma parcial de Fourier da entrada;
- a resposta ideal RC no capacitor;
- a reconstrução harmônica usando o ganho definido por retas inseridas pelo aluno;
- o ganho teórico RC e o ganho ajustado em escala log-log;
- o espectro harmônico no mesmo painel do gráfico de ganho.

---

## Sumário

1. [Sobre o projeto](#sobre-o-projeto)
2. [Contexto didático](#contexto-didático)
3. [O que o programa mostra](#o-que-o-programa-mostra)
4. [Fundamentação teórica](#fundamentação-teórica)
5. [Interface atual](#interface-atual)
6. [Como usar](#como-usar)
7. [Estrutura sugerida do repositório](#estrutura-sugerida-do-repositório)
8. [Status atual](#status-atual)
9. [Uso didático esperado](#uso-didático-esperado)
10. [Limitações do modelo](#limitações-do-modelo)
11. [Próximos passos](#próximos-passos)
12. [Como citar](#como-citar)
13. [Créditos](#créditos)

---

## Sobre o projeto

Este projeto foi desenvolvido como material de apoio para a atividade **Exp3Atv0** da disciplina **4302213 — Física Experimental III**, no Instituto de Física da Universidade de São Paulo.

O objetivo é oferecer uma ferramenta visual para conectar três descrições de um mesmo fenômeno:

1. a forma de onda observada no domínio do tempo;
2. a decomposição harmônica por série de Fourier;
3. a resposta em frequência de um circuito RC passa-baixa.

O programa não busca substituir a análise experimental. Ele serve como uma ponte conceitual entre as medições de bancada e a interpretação física dos sinais.

---

## Contexto didático

Uma onda quadrada ideal possui transições abruptas. Essas transições exigem harmônicos de frequência cada vez mais alta na sua decomposição de Fourier.

Quando uma onda quadrada é aplicada a um filtro RC passa-baixa medido no capacitor, os harmônicos mais altos são mais atenuados. Por isso, a saída observada no capacitor tende a ficar mais suave, com bordas menos abruptas e dependência clara da razão entre a frequência fundamental da onda quadrada e a frequência de corte do circuito.

A atividade permite discutir:

- por que uma onda quadrada exige muitos harmônicos;
- por que harmônicos altos afetam principalmente as bordas da onda;
- por que um filtro passa-baixa arredonda a saída;
- como um gráfico de ganho em função da frequência se traduz em uma forma de onda no tempo;
- como comparar uma curva esperada ideal com uma curva reconstruída a partir de parâmetros medidos.

---

## O que o programa mostra

A interface atual trabalha com três áreas principais:

```text
linha superior:
    configurações | ganho passa-baixa + espectro harmônico

linha inferior:
    gráfico temporal largo
```

No gráfico temporal, aparecem:

- **Entrada: onda quadrada**  
  Onda quadrada ideal aplicada ao circuito.

- **Entrada por Fourier**  
  Soma parcial da série de Fourier da onda quadrada. Serve para mostrar como a onda quadrada é reconstruída por harmônicos ímpares.

- **Saída ideal RC: carga/descarga**  
  Resposta temporal esperada para o capacitor em um circuito RC ideal, calculada por trechos de carga e descarga exponencial. Essa curva aparece como referência de fundo.

- **Saída por Fourier + ganho ajustado**  
  Reconstrução harmônica usando o ganho definido pelo aluno por meio de duas retas em escala log-log.

- **Harmônicos individuais**  
  Visualização opcional dos primeiros harmônicos individuais usados na composição da onda.

No gráfico de ganho, aparecem:

- ganho RC ideal como referência;
- ganho definido pelas retas do aluno;
- pontos correspondentes aos harmônicos usados na reconstrução;
- frequência de corte ideal;
- interseção das retas;
- espectro harmônico no eixo direito.

---

## Fundamentação teórica

### Série de Fourier da onda quadrada

Uma onda quadrada ímpar de amplitude normalizada pode ser aproximada por:

```math
v_{\mathrm{in},M}(t)
=
\frac{4V_0}{\pi}
\sum_{k=1}^{M}
\frac{
\sin\!\left[2\pi(2k-1)f_0t\right]
}{
2k-1
}.
```

Aqui:

- `V0` é a amplitude de pico;
- `f0` é a frequência fundamental;
- `M` é o número de harmônicos ímpares incluídos;
- o índice `2k-1` seleciona os harmônicos ímpares.

As frequências harmônicas são:

```math
f_k = (2k-1) f_0.
```

---

### Ganho passa-baixa RC ideal

Para um circuito RC passa-baixa medido no capacitor:

```math
H_{RC}(f)
=
\frac{1}{1+j2\pi fRC}.
```

O módulo do ganho é:

```math
G_{RC}(f)
=
|H_{RC}(f)|
=
\frac{1}{\sqrt{1+(2\pi fRC)^2}}.
```

A frequência de corte é:

```math
f_c
=
\frac{1}{2\pi RC}.
```

A fase ideal do circuito é:

```math
\phi_{RC}(f)
=
-\arctan(2\pi fRC).
```

---

### Ganho definido pelo aluno

O programa permite que o aluno modele o ganho medido em bancada por duas retas em escala log-log:

```math
\log_{10}(G)
=
a\log_{10}(f)+b.
```

A interface usa duas retas:

```math
\log_{10}(G_1)
=
a_1\log_{10}(f)+b_1,
```

```math
\log_{10}(G_2)
=
a_2\log_{10}(f)+b_2.
```

O envelope usado pelo programa é o menor valor entre as duas retas, com o ganho limitado ao intervalo físico-operacional usado na simulação:

```math
G_{\mathrm{aluno}}(f)
=
\min(G_1(f),G_2(f)).
```

Na prática, isso permite representar uma região de platô em baixas frequências e uma região de queda em altas frequências.

---

### Reconstrução temporal com ganho ajustado

A curva vermelha é reconstruída aplicando o ganho definido pelo aluno a cada harmônico:

```math
v_{\mathrm{fit},M}(t)
=
\frac{4V_0}{\pi}
\sum_{k=1}^{M}
G_{\mathrm{aluno}}(f_k)
\frac{
\sin\!\left[2\pi f_kt\right]
}{
2k-1
}.
```

A interface também possui uma opção para ligar ou desligar a fase ideal RC nessa reconstrução.

Com **fase RC desligada**, se:

```math
a_1=b_1=a_2=b_2=0,
```

então:

```math
G_{\mathrm{aluno}}(f)=1
```

e a curva vermelha coincide com a soma de Fourier da entrada.

Com **fase RC ligada**, as amplitudes continuam vindo do ganho definido pelo aluno, mas cada harmônico recebe a fase ideal do circuito RC.

---

## Interface atual

A versão atual da interface inclui:

- janela inicial de escolha da escala visual;
- layout em duas linhas:
  - configurações e ganho na parte superior;
  - gráfico temporal largo na parte inferior;
- slider de `M` com modo de confirmação ao soltar o mouse;
- caixa de texto para digitar `M` diretamente;
- botões para escolher circuito, frequência e camadas exibidas;
- retas ajustáveis por parâmetros `a1`, `b1`, `a2`, `b2`;
- botão para usar retas associadas ao RC ideal;
- botão para ligar/desligar a fase ideal RC na reconstrução vermelha;
- indicador visual de processamento para ações matemáticas e de interface.

### Circuitos pré-configurados

O programa inclui dois casos didáticos:

| R | C | Observação |
|---:|---:|---|
| `1 kΩ` | `0,47 µF` | caso de referência |
| `47 Ω` | `47 µF` | caso alternativo com frequências ajustadas pela razão `f0/fc` |

### Frequências de interesse

Para o circuito `1 kΩ`, as frequências preparadas são:

| Regime | Frequência |
|---|---:|
| baixo | `72 Hz` |
| aproximadamente corte | `360 Hz` |
| alto | `7,2 kHz` |

Para o circuito `47 Ω`, as frequências são ajustadas automaticamente para preservar aproximadamente as mesmas razões `f0/fc`.

---

## Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC.git
cd Lab3-2026-Exp3Atv0-Fourier-Filtro_RC
```

### 2. Criar ambiente virtual

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

### 3. Instalar dependências

```bash
pip install numpy matplotlib
```

Opcionalmente, crie um `requirements.txt` com:

```text
numpy
matplotlib
```

e instale com:

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
python fourier_onda_quadrada_filtro_rc.py
```

Ao iniciar, o programa abre uma janela para escolher a escala visual. Depois disso, a janela principal é aberta com a escala travada para a sessão.

---

## Estrutura sugerida do repositório

```bash
.
├── README.md
├── LICENSE
├── .gitignore
├── fourier_onda_quadrada_filtro_rc.py
├── requirements.txt
├── figures/
│   └── README.md
├── data/
│   ├── examples/
│   └── raw/
└── docs/
```

Arquivos e pastas sugeridos:

- `fourier_onda_quadrada_filtro_rc.py`  
  Script principal da simulação.

- `requirements.txt`  
  Dependências mínimas do projeto.

- `figures/`  
  Figuras exportadas ou imagens usadas na documentação.

- `data/examples/`  
  Dados pequenos de exemplo, caso sejam adicionados em versões futuras.

- `data/raw/`  
  Dados brutos locais. Recomenda-se não versionar arquivos grandes ou dados experimentais ainda não tratados.

- `docs/`  
  Materiais didáticos complementares, roteiro de aula ou explicações adicionais.

---

## Status atual

O projeto está em fase de protótipo didático funcional.

A versão atual já possui:

- decomposição de onda quadrada por série de Fourier;
- resposta ideal RC por carga/descarga exponencial;
- ganho RC ideal em escala log-log;
- ganho ajustável por duas retas inseridas pelo aluno;
- reconstrução temporal com ganho ajustado;
- opção de fase RC ideal ligada/desligada;
- espectro harmônico integrado ao gráfico de ganho;
- interface com controle de escala visual inicial;
- otimizações de responsividade para o slider;
- indicador de processamento;
- layout refinado para uso em tela widescreen.

Ainda há pontos em evolução:

- refinamento fino de alinhamento da interface;
- teste em diferentes versões de Python, Matplotlib e backends gráficos;
- possível separação futura entre núcleo físico e camada de interface;
- entrada de dados experimentais por CSV;
- documentação pedagógica para alunos.

---

## Uso didático esperado

Durante a atividade, espera-se que o estudante explore perguntas como:

1. Quantos harmônicos são necessários para a onda se parecer com uma onda quadrada?
2. O que acontece com a forma da onda quando harmônicos altos são atenuados?
3. Como a posição dos harmônicos no gráfico de ganho explica a forma da onda no tempo?
4. Como as retas medidas em escala log-log afetam a reconstrução temporal?
5. Por que a fase do filtro altera a comparação entre a reconstrução harmônica e a resposta temporal ideal?
6. Em quais regimes a saída no capacitor se aproxima de uma carga/descarga exponencial simples?
7. O que muda quando a frequência fundamental está abaixo, próxima ou acima da frequência de corte?

---

## Limitações do modelo

Este programa é didático e possui simplificações.

Entre as principais limitações:

- o circuito RC é tratado como ideal;
- a onda quadrada é idealizada, sem limitações reais de gerador;
- a reconstrução por Fourier é truncada;
- a série apresenta fenômeno de Gibbs próximo às descontinuidades;
- as retas do aluno representam apenas o módulo do ganho;
- a opção de fase usa a fase ideal RC, não uma fase medida em bancada;
- não há, por enquanto, importação direta de dados experimentais;
- o ajuste por duas retas é uma aproximação didática do ganho passa-baixa.

---

## Próximos passos

Possíveis melhorias futuras:

- [ ] criar `requirements.txt`;
- [ ] separar funções físicas/matemáticas da classe de interface;
- [ ] criar testes simples para funções de Fourier e ganho;
- [ ] permitir importação de dados experimentais por `.csv`;
- [ ] interpolar ganho medido pelos alunos;
- [ ] permitir comparação entre ganho medido, ganho ajustado e ganho ideal;
- [ ] adicionar exportação automática de figuras;
- [ ] adicionar roteiro didático para alunos;
- [ ] adicionar imagens da interface ao README;
- [ ] criar `CITATION.cff`;
- [ ] revisar layout da interface em escalas 100%, 125%, 150% e 200%;
- [ ] documentar limitações associadas à fase.

---

## Como citar

Se este código for útil em relatório, aula, monitoria ou material didático, cite:

> **Araujo Junior, G. R.** (2026). *Onda Quadrada, Fourier e Filtro RC Passa-Baixa: Exp3Atv0*. GitHub Repository.  
> `https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC`

Quando o arquivo `CITATION.cff` estiver disponível, dê preferência à citação indicada nele.

---

## Créditos

- **Desenvolvedor:** Guterman Rodrigues de Araujo Junior
- **Instituição:** Instituto de Física da Universidade de São Paulo
- **Disciplina:** 4302213 — Física Experimental III
- **Atividade:** Experimento 3 — Atividade 0
- **Finalidade:** material didático em desenvolvimento para apoio à visualização de Fourier, resposta em frequência e filtro RC passa-baixa.

---

<div align="center">
  <sub>Material didático em desenvolvimento para apoio à Física Experimental III — IFUSP.</sub>
</div>
