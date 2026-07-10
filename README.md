# 📡 Onda Quadrada, Série de Fourier e Filtro RC Passa-Baixa

## Instituto de Física da Universidade de São Paulo (IFUSP)

### Simulador didático para a Exp3Atv0 — Física Experimental III — IFUSP

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-c%C3%A1lculo%20num%C3%A9rico-4D77CF?style=for-the-badge\&logo=numpy\&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-interface%20gr%C3%A1fica-11557C?style=for-the-badge)
![Status](https://img.shields.io/badge/status-prot%C3%B3tipo%20did%C3%A1tico-yellow?style=for-the-badge)
![Versão](https://img.shields.io/badge/vers%C3%A3o-1.5.0--alpha-red?style=for-the-badge)

</div>

---

## Visão geral

Este repositório contém um programa interativo em Python para estudar como uma onda quadrada é representada por uma série de Fourier e como um circuito RC passa-baixa modifica cada termo harmônico.

O programa foi desenvolvido como material de apoio para a disciplina **4302213 — Física Experimental III**, do Instituto de Física da Universidade de São Paulo, no contexto da **Exp3Atv0**.

A proposta didática é conectar três descrições do mesmo experimento:

1. **domínio do tempo**, observado no osciloscópio;
2. **domínio da frequência**, descrito pelo ganho do circuito;
3. **decomposição harmônica**, obtida pela série de Fourier.

O fluxo conceitual é:

```text
onda quadrada
    ↓
harmônicos ímpares da série de Fourier
    ↓
ganho e fase avaliados em cada frequência harmônica
    ↓
novas amplitudes e fases
    ↓
reconstrução da saída no domínio do tempo
```

A medição no osciloscópio é a referência experimental. O programa fornece modelos para interpretar essa medição, comparar aproximações e compreender quais hipóteses físicas foram utilizadas.

---

## Sumário

* [Objetivos didáticos](#objetivos-didáticos)
* [Funcionalidades atuais](#funcionalidades-atuais)
* [Interface](#interface)
* [Fundamentação física](#fundamentação-física)
* [Modelo de ganho obtido das retas do aluno](#modelo-de-ganho-obtido-das-retas-do-aluno)
* [Significado das curvas e dos pontos](#significado-das-curvas-e-dos-pontos)
* [Termo harmônico genérico](#termo-harmônico-genérico)
* [Como usar](#como-usar)
* [Instalação](#instalação)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Estratégias de desempenho](#estratégias-de-desempenho)
* [Limitações](#limitações)
* [Validações esperadas](#validações-esperadas)
* [Próximos passos](#próximos-passos)
* [Como citar](#como-citar)
* [Créditos](#créditos)

---

## Objetivos didáticos

O programa permite investigar:

* como uma onda quadrada é construída a partir de senos;
* por que aparecem somente harmônicos ímpares;
* como o número de termos $M$ altera a reconstrução;
* como o ganho passa-baixa atenua os harmônicos mais altos;
* como a fase altera a soma temporal dos termos;
* por que a saída no capacitor fica mais suave;
* como relacionar retas ajustadas em escala log-log com uma curva de ganho contínua;
* como os pontos $G(f_k)$ do gráfico de ganho se transformam em amplitudes $A_kG(f_k)$ no espectro;
* como comparar o circuito RC teórico com um modelo inferido das medições de bancada.

---

## Funcionalidades atuais

A versão atual inclui:

* onda quadrada ideal de entrada;
* reconstrução da entrada por série de Fourier;
* resposta ideal do capacitor por carga e descarga exponencial;
* modelo teórico do ganho de um circuito RC ideal;
* duas retas ajustáveis em escala log-log;
* curva suave de ganho inferida das duas retas;
* reconstrução temporal usando o ganho inferido pelo aluno;
* fase estimada opcional a partir da interseção das retas;
* espectro harmônico em painel separado;
* identificação dos ganhos avaliados nas frequências harmônicas;
* painel didático com a forma genérica do termo harmônico;
* valores numéricos do último termo incluído, $k=M$;
* escolha de circuito e frequência de interesse;
* controle de $M$ por slider, botões e caixa de texto;
* escala visual escolhida antes da abertura da janela principal;
* indicador visual `Processando...`;
* atualização otimizada do slider por confirmação ao soltar o mouse;
* suporte a diferentes escalas de exibição.

---

## Interface

A interface é organizada em quatro regiões:

```text
┌──────────────────────────────┬──────────────────────────────────┐
│ Configurações                │ Ganho e espectro harmônico       │
│                              │ em painéis separados             │
├─────────────────────────────────────────────────────────────────┤
│ Forma genérica e valores do termo harmônico k=M                │
├─────────────────────────────────────────────────────────────────┤
│ Gráfico temporal largo                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Configurações

A área de configurações permite selecionar:

* circuito:

  * $R=1,\mathrm{k\Omega}$, $C=0{,}47,\mathrm{\mu F}$;
  * $R=47,\Omega$, $C=47,\mathrm{\mu F}$;
* frequência fundamental:

  * regime abaixo do corte;
  * região próxima do corte;
  * regime acima do corte;
* número de termos $M$;
* elementos que devem ser exibidos;
* parâmetros $a_1,b_1,a_2,b_2$ das retas;
* fase estimada ligada ou desligada;
* carregamento das assíntotas teóricas de um RC ideal.

### Controle de $M$

O slider foi limitado à região didaticamente mais útil:

```text
1 ≤ M ≤ 15
```

A caixa de texto permite inserir valores maiores:

```text
1 ≤ M ≤ 200
```

O slider só confirma o valor ao soltar o mouse. Durante o arraste, apenas seu elemento visual é atualizado por blitting.

---

## Fundamentação física

## Onda quadrada ideal

A entrada é modelada por:

$$
v_e(t)=V_0,\operatorname{sgn}!\left[\sin(2\pi f_0t)\right].
$$

Aqui:

* $V_0$ é a amplitude de pico;
* $f_0$ é a frequência fundamental.

---

## Série de Fourier

A soma truncada com $M$ termos ímpares é:

$$
v_{e,M}(t)
==========

\frac{4V_0}{\pi}
\sum_{k=1}^{M}
\frac{
\sin!\left[2\pi(2k-1)f_0t\right]
}{
2k-1
}.
$$

Definindo:

$$
n_k=2k-1,
$$

as frequências harmônicas são:

$$
f_k=n_kf_0=(2k-1)f_0.
$$

A amplitude do $k$-ésimo termo da entrada é:

$$
A_k=\frac{4V_0}{\pi n_k}.
$$

Como a soma é truncada, aparecem oscilações próximas às descontinuidades, associadas ao fenômeno de Gibbs.

---

## Circuito RC ideal

Para um circuito RC série, medido sobre o capacitor:

$$
H_{RC}(f)
=========

\frac{1}{1+j2\pi fRC}.
$$

O módulo do ganho é:

$$
G_{RC}(f)
=========

# \left|H_{RC}(f)\right|

\frac{1}{
\sqrt{1+(2\pi fRC)^2}
}.
$$

A fase é:

$$
\phi_{RC}(f)
============

-\arctan(2\pi fRC).
$$

A frequência de corte é:

$$
f_c=\frac{1}{2\pi RC}.
$$

Na frequência de corte:

$$
G_{RC}(f_c)=\frac{1}{\sqrt{2}}\approx0{,}707.
$$

---

## Modelo de ganho obtido das retas do aluno

A partir das medições de bancada, o aluno pode calcular:

$$
G(f)=\left|\frac{V_C(f)}{V_e(f)}\right|.
$$

Em escala log-log:

$$
x=\log_{10}(f),
\qquad
y=\log_{10}(G).
$$

Duas regiões podem ser ajustadas por retas:

$$
\log_{10}G_1(f)=a_1\log_{10}f+b_1,
$$

$$
\log_{10}G_2(f)=a_2\log_{10}f+b_2.
$$

Em escala linear:

$$
G_1(f)=10^{a_1\log_{10}f+b_1},
$$

$$
G_2(f)=10^{a_2\log_{10}f+b_2}.
$$

### Curva suave inferida

Em vez de usar o mínimo abrupto entre as retas, o programa constrói:

$$
G_{\mathrm{aluno}}(f)
=====================

\left[
G_1(f)^{-p}
+
G_2(f)^{-p}
\right]^{-1/p}.
$$

A versão atual utiliza:

$$
p=2.
$$

Para as assíntotas ideais:

$$
G_1(f)=1,
$$

$$
G_2(f)=\frac{f_c}{f},
$$

a expressão se reduz a:

$$
G_{\mathrm{aluno}}(f)
=====================

\frac{1}{
\sqrt{1+(f/f_c)^2}
},
$$

que coincide com o módulo exato do RC de primeira ordem.

Essa equivalência foi verificada numericamente no desenvolvimento, com diferença limitada ao erro de ponto flutuante.

### Interseção das retas

A frequência de interseção é:

$$
f_\times
========

10^{
\frac{b_2-b_1}{a_1-a_2}
}.
$$

Quando a fase estimada está ligada, o programa usa:

$$
\phi_{\mathrm{aluno}}(f)
========================

-\arctan!\left(\frac{f}{f_\times}\right).
$$

Essa fase não foi medida diretamente. Ela é uma aproximação de primeira ordem inferida das próprias retas.

### Observação importante

A combinação suave pressupõe duas assíntotas complementares. Se as duas retas forem idênticas, a expressão não é igual ao mínimo exato delas. Para $G_1=G_2=1$ e $p=2$:

$$
G_{\mathrm{aluno}}=\frac{1}{\sqrt{2}}.
$$

Portanto, a condição $a_1=b_1=a_2=b_2=0$ não representa mais um teste de ganho unitário na versão atual. O modelo deve ser interpretado como uma interpolação suave entre uma região de platô e uma região de queda.

---

## Significado das curvas e dos pontos

Este é o ponto central para interpretar corretamente o programa.

## Painel de ganho

### Linha cinza

$$
G_{RC}(f)
$$

É o ganho teórico do circuito RC calculado a partir dos valores nominais de $R$ e $C$.

Ela serve como referência idealizada.

### Linhas vermelhas tracejadas

$$
G_1(f)
\quad\text{e}\quad
G_2(f)
$$

São as duas retas inseridas pelo aluno.

Elas representam as assíntotas ajustadas aos dados experimentais.

### Linha vermelha contínua

$$
G_{\mathrm{aluno}}(f)
$$

É a curva suave construída a partir das duas retas.

Essa é a curva usada na reconstrução temporal vermelha.

### Círculos vazados

$$
G_{RC}(f_k)
$$

São os valores do ganho teórico avaliados apenas nas frequências harmônicas:

$$
f_k=(2k-1)f_0.
$$

Eles não são novos dados experimentais e não formam um terceiro modelo.

### Quadrados vermelhos

$$
G_{\mathrm{aluno}}(f_k)
$$

São os fatores que o programa realmente aplica às amplitudes dos termos da série de Fourier.

Em outras palavras:

$$
A_{k,\mathrm{saída}}
====================

A_kG_{\mathrm{aluno}}(f_k).
$$

Alguns pontos são identificados como:

```text
f0, 3f0, 5f0, ...
```

para mostrar quais frequências da série estão sendo amostradas no gráfico de ganho.

---

## Painel de espectro

O espectro foi colocado em um eixo próprio porque seus pontos representam **amplitudes**, e não ganhos.

### Entrada

$$
A_k
===

\frac{4V_0}{\pi(2k-1)}.
$$

### Saída teórica

$$
A_kG_{RC}(f_k).
$$

### Saída simulada a partir das retas

$$
A_kG_{\mathrm{aluno}}(f_k).
$$

Portanto:

```text
gráfico de ganho:
    informa quanto cada frequência é multiplicada;

espectro:
    informa qual é a amplitude resultante de cada harmônico.
```

A versão atual ainda não importa automaticamente os pontos medidos da bancada. Os marcadores exibidos são valores dos modelos nas frequências harmônicas. A importação de dados experimentais é uma evolução futura prevista.

---

## Gráfico temporal

As curvas principais são:

### Azul — onda quadrada ideal

Entrada ideal aplicada ao circuito.

### Verde tracejada — Fourier da entrada

Soma truncada com $M$ termos.

### Laranja — resposta RC ideal

Resposta por carga e descarga exponencial em regime periódico permanente.

É a referência temporal teórica.

### Vermelha — saída simulada pelo aluno

Reconstrução:

$$
v_{\mathrm{aluno},M}(t)
=======================

\sum_{k=1}^{M}
A_kG_{\mathrm{aluno}}(f_k)
\sin!\left(
2\pi f_kt+\phi_{\mathrm{aluno}}(f_k)
\right).
$$

Com fase desligada:

$$
\phi_{\mathrm{aluno}}(f_k)=0.
$$

Com fase estimada ligada:

$$
\phi_{\mathrm{aluno}}(f_k)
==========================

-\arctan!\left(\frac{f_k}{f_\times}\right).
$$

O objetivo é comparar qualitativamente essa curva com a forma de onda observada no osciloscópio.

---

## Termo harmônico genérico

O programa mostra explicitamente:

$$
v_k(t)
======

A_kG(f_k)
\sin!\left(
\omega_kt+\phi_k
\right).
$$

Com:

$$
n_k=2k-1,
$$

$$
f_k=n_kf_0,
$$

$$
\omega_k=2\pi f_k,
$$

$$
A_k=\frac{4V_0}{\pi n_k}.
$$

Também são exibidos os valores numéricos do último termo incluído:

```text
k = M
nM = 2M − 1
fM
ωM
AM
G(fM)
AM·G(fM)
φM
```

A distinção de notação é:

* $M$: número total de termos incluídos;
* $k$: índice de um termo;
* $n_k=2k-1$: ordem harmônica ímpar.

---

## Como usar

1. Escolha a escala visual inicial.
2. Selecione o circuito.
3. Selecione a frequência fundamental.
4. Defina o número de termos $M$.
5. Insira os coeficientes das duas retas:

   * $a_1,b_1$;
   * $a_2,b_2$.
6. Observe:

   * as retas;
   * a curva suave inferida;
   * os valores do ganho nas frequências harmônicas;
   * o espectro;
   * a reconstrução temporal.
7. Ligue ou desligue a fase estimada.
8. Compare a curva vermelha:

   * com a referência teórica laranja;
   * com a forma de onda medida no osciloscópio.

### Retas em decibéis

Se o ajuste foi feito como:

$$
G_{\mathrm{dB}}
===============

A\log_{10}(f)+B,
$$

e:

$$
G_{\mathrm{dB}}=20\log_{10}(G),
$$

então:

$$
a=\frac{A}{20},
\qquad
b=\frac{B}{20}.
$$

---

## Instalação

## Requisitos

* Python 3.10 ou superior;
* NumPy;
* Matplotlib;
* Tkinter disponível na instalação do Python para a janela inicial de escala.

## Clonar o repositório

```bash
git clone https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC.git
cd Lab3-2026-Exp3Atv0-Fourier-Filtro_RC
```

## Criar ambiente virtual

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Instalar dependências

```bash
python -m pip install --upgrade pip
python -m pip install numpy matplotlib
```

## Executar

```bash
python fourier_onda_quadrada_filtro_rc.py
```

---

## Estrutura do projeto

Estrutura recomendada:

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── fourier_onda_quadrada_filtro_rc.py
├── docs/
│   ├── teoria.md
│   └── imagens/
├── data/
│   ├── exemplos/
│   └── experimentais/
└── tests/
```

### Arquivo principal

```text
fourier_onda_quadrada_filtro_rc.py
```

Contém:

* modelos físicos;
* funções matemáticas;
* construção da interface;
* lógica de interação;
* otimizações de renderização.

---

## Estratégias de desempenho

A interface Matplotlib recebeu otimizações específicas:

* escala visual calculada uma única vez;
* tema visual estático;
* ausência de reescalonamento durante as interações;
* botões simples no lugar de widgets mais frágeis;
* harmônicos individuais agrupados em `LineCollection`;
* slider com confirmação ao soltar;
* blitting local durante o arraste;
* `TextBox.set_val()` evitado em sincronizações internas;
* apenas um redraw completo ao fim de cada alteração;
* indicador `Processando...` desenhado por blitting quando possível;
* legendas criadas uma única vez;
* atualização seletiva de curvas e textos.

O custo restante depende do backend gráfico, da resolução da tela, da escala do sistema e da versão do Matplotlib.

---

## Limitações

* O circuito de referência é ideal.
* A onda quadrada de entrada é idealizada.
* A série de Fourier é truncada.
* Há fenômeno de Gibbs nas descontinuidades.
* Os valores nominais de $R$ e $C$ não incluem tolerâncias automaticamente.
* A curva suave do aluno pressupõe comportamento de primeira ordem.
* A fase estimada não é uma fase experimental medida.
* O programa ainda não importa pontos experimentais diretamente.
* O osciloscópio, gerador, cabos, impedâncias, ruído e largura de banda real podem produzir diferenças em relação ao modelo.
* A combinação suave com $p=2$ é fisicamente adequada para assíntotas de um RC de primeira ordem, mas não representa automaticamente circuitos de ordem superior.
* O programa é um recurso didático, não um instrumento de ajuste metrológico.

---

## Validações esperadas

### Baixas frequências

Para:

$$
f_0\ll f_c,
$$

os primeiros harmônicos devem sofrer pouca atenuação e a saída tende a preservar a forma quadrada.

### Próximo ao corte

Para:

$$
f_0\approx f_c,
$$

a fundamental já é atenuada e defasada, e os harmônicos superiores sofrem atenuação maior.

### Altas frequências

Para:

$$
f_0\gg f_c,
$$

a saída apresenta forte suavização e pode se aproximar do regime integrador.

### Assíntotas ideais

Com:

$$
a_1=0,\quad b_1=0,
$$

$$
a_2=-1,\quad b_2=\log_{10}(f_c),
$$

a curva suave com $p=2$ deve coincidir com o módulo RC ideal, dentro do erro numérico de ponto flutuante.

---

## Próximos passos

* [ ] importar pontos experimentais de ganho por CSV;
* [ ] mostrar os pontos medidos sobre as curvas teórica e inferida;
* [ ] permitir ajuste automático das duas retas;
* [ ] permitir ajuste de $p$;
* [ ] importar fase experimental;
* [ ] separar o núcleo físico da camada de interface;
* [ ] criar testes automatizados;
* [ ] adicionar exportação de figuras e parâmetros;
* [ ] adicionar arquivo `requirements.txt`;
* [ ] adicionar `CITATION.cff`;
* [ ] incluir capturas de tela no README;
* [ ] documentar um roteiro completo para uso em aula;
* [ ] avaliar modelos de ordem superior.

---

## Como citar

> Araujo Junior, G. R. (2026). *Onda Quadrada, Série de Fourier e Filtro RC Passa-Baixa: simulador didático para a Exp3Atv0*. Repositório de software.

Repositório:

```text
https://github.com/gutermanjunior/Lab3-2026-Exp3Atv0-Fourier-Filtro_RC
```

---

## Créditos

* **Desenvolvedor:** Guterman Rodrigues de Araujo Junior
* **Instituição:** Instituto de Física da Universidade de São Paulo
* **Disciplina:** 4302213 — Física Experimental III
* **Atividade:** Experimento 3 — Atividade 0
* **Finalidade:** apoio didático ao estudo de série de Fourier, resposta em frequência e circuito RC passa-baixa.

---

<div align="center">

**Material didático em desenvolvimento — IFUSP — 2026**

</div>
