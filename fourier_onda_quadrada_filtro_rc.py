# =============================================================================
# Arquivo: fourier_onda_quadrada_filtro_rc_v16_responsivo.py
# Título: Onda quadrada, série de Fourier e filtro RC passa-baixa
#
# Projeto:
#     Lab3-2026-Exp3Atv0-Fourier-Filtro_RC
#
# Contexto didático:
#     Material de apoio para a disciplina 4302213 - Física Experimental III
#     do Instituto de Física da Universidade de São Paulo (IFUSP).
#
# Descrição:
#     Este programa compara diferentes descrições de uma onda quadrada aplicada
#     a um circuito RC passa-baixa:
#
#         1. onda quadrada ideal de entrada;
#         2. resposta temporal do capacitor por carga e descarga exponencial;
#         3. reconstrução da entrada por série de Fourier;
#         4. reconstrução da saída usando os harmônicos da onda quadrada
#            multiplicados pela função de transferência do filtro RC;
#         5. gráfico de ganho em função da frequência;
#         6. espectro harmônico antes e depois da filtragem.
#
# Objetivo didático:
#     Mostrar que a forma temporal de uma onda quadrada está ligada ao seu
#     conteúdo harmônico e que um filtro passa-baixa modifica a onda porque
#     atenua e defasa cada harmônico de forma dependente da frequência.
#
#     A ideia central é:
#
#         onda quadrada no tempo
#             -> harmônicos ímpares de Fourier
#             -> ganho e fase do filtro RC em cada harmônico
#             -> reconstrução da tensão no capacitor
#
# Versão:
#     1.3.0-alpha
#
# Estado:
#     Código em desenvolvimento.
#
# Mudança arquitetural desta versão:
#     A escala visual é escolhida antes da abertura da janela principal e vira
#     um "tema visual" estático. Isso evita que a interface fique recalculando
#     fontes, larguras, marcadores, posições de widgets e legendas durante o uso.
#
#     Durante as interações normais, o programa atualiza apenas os dados dos
#     gráficos, a visibilidade de curvas e textos simples. A escala NÃO é
#     reaplicada durante o uso.
#
# Autor:
#     Guterman Rodrigues de Araujo Junior
#
# Data:
#     2026-07-08
#
# Dependências:
#     Python >= 3.10
#     numpy
#     matplotlib
#
# Instalação das dependências:
#     pip install numpy matplotlib
#
# Execução:
#     python fourier_onda_quadrada_filtro_rc_v16_responsivo.py
#
# Modelos físicos usados:
#
#     1. Onda quadrada ideal:
#
#            v_e(t) = V0 sign[sin(2π f0 t)]
#
#     2. Série de Fourier truncada da onda quadrada ímpar:
#
#            v_e,M(t) = (4 V0 / π) Σ_{k=1}^{M}
#                       sin[2π(2k - 1)f0 t] / (2k - 1)
#
#        Apenas harmônicos ímpares aparecem:
#
#            f_k = (2k - 1) f0.
#
#     3. Função de transferência ideal do filtro RC passa-baixa, medida sobre
#        o capacitor:
#
#            H_RC(f) = 1 / [1 + j 2π f R C].
#
#        Módulo:
#
#            |H_RC(f)| = 1 / sqrt[1 + (2π f R C)^2].
#
#        Fase:
#
#            φ(f) = -arctan(2π f R C).
#
#     4. Saída por Fourier:
#
#            v_C,M(t) = Σ A_k |H_RC(f_k)|
#                       sin[2π f_k t + arg H_RC(f_k)].
#
#     5. Retas ajustadas em escala log-log:
#
#            log10(G) = a log10(f) + b.
#
#        O envelope passa-baixa é aproximado pelo menor valor entre as duas
#        retas. Essa ferramenta foi incluída para permitir comparação com
#        retas obtidas pelos alunos a partir do gráfico experimental de ganho.
#
# Limitações:
#     - O modelo RC é ideal.
#     - A onda quadrada ideal tem descontinuidades. A série de Fourier converge
#       para o valor médio nos pontos de salto e apresenta o fenômeno de Gibbs.
#     - A solução por carga/descarga considera regime periódico permanente.
#     - As retas ajustadas em log-log são uma aproximação didática do ganho.
#
# Estratégia de desempenho:
#     - Escala visual aplicada uma única vez.
#     - Tema visual calculado uma única vez.
#     - RadioButtons e CheckButtons foram substituídos por Buttons simples.
#     - Harmônicos individuais são desenhados com LineCollection, não com
#       centenas de Line2D.
#     - O gráfico temporal desenha no máximo MAX_HARMONICOS_INDIVIDUAIS_DESENHADOS
#       harmônicos individuais; a soma de Fourier e o espectro continuam usando
#       o M completo.
#     - As legendas são criadas uma vez e não são reconstruídas a cada update.
#     - A sincronização entre slider e caixa de texto de M evita redraws
#       intermediários e não chama Slider.set_val() quando a ação já veio do
#       próprio slider.
#     - TextBox.set_val() não é usado mais na sincronização de M, porque
#       esse método chama renderização síncrona do cursor do TextBox em
#       algumas versões do Matplotlib. A atualização visual é feita por
#       text_disp.set_text(), deixando apenas um draw_idle() no fim.
#     - O slider de M agora funciona em modo commit: durante o arraste, ele
#       não recalcula nem redesenha os gráficos; ao soltar o mouse, a nova
#       escolha de M é aplicada uma única vez.
#     - A caixa de texto de M aplica o valor tanto com Enter quanto quando
#       o usuário clica fora da caixa.
#     - Durante o arraste, a parte visual do slider é atualizada por blitting
#       apenas no eixo do slider; os gráficos físicos continuam sendo
#       atualizados somente ao soltar o mouse.
#     - O slider de M vai até 100 para dar mais resolução visual aos valores
#       baixos. A caixa de texto continua aceitando M até N_MAX.
#     - O valor numérico nativo do Slider foi ocultado para não sobrepor a
#       caixa de texto M; a caixa M fica como o mostrador numérico principal.
#     - Layout principal reorganizado em duas linhas:
#         linha superior: configurações | ganho + espectro;
#         linha inferior: gráfico de tensão no tempo ocupando toda a largura.
#     - A curva temporal vermelha passa a usar apenas o módulo do ganho
#       ajustado pelas retas inseridas pelo aluno, sem impor a fase teórica do
#       RC. Assim, se a=b=0 nas duas retas, G=1 para todas as frequências e a
#       curva vermelha coincide com a soma de Fourier da entrada.
#     - O gráfico de ganho dá maior destaque à curva definida pelo aluno;
#       a curva RC ideal fica como referência visual secundária.
#     - Adicionada configuração para ligar/desligar a fase ideal RC na
#       reconstrução temporal vermelha. Com fase desligada, se a=b=0 nas duas
#       retas, a curva vermelha coincide com a Fourier da entrada. Com fase
#       ligada, as amplitudes vêm do ganho do aluno e as fases vêm do RC ideal.
#     - Painel de configurações realinhado: controles superiores, resumo,
#       controle de M e parâmetros das retas foram separados em faixas
#       verticais para evitar sobreposição visual.
#     - Refinamento de alinhamento do painel de configurações: títulos dos
#       grupos centralizados pelo centro geométrico dos botões, bloco do ganho
#       do aluno separado em título/fórmula/parâmetros, caixas numéricas com
#       texto centralizado, e botões de fase/reset alinhados em coluna própria.
#     - Ajuste adicional no bloco vermelho do ganho do aluno: título e fórmula
#       foram colocados em faixas separadas para evitar sobreposição em 100%,
#       200% e outras escalas visuais.
#     - Retorno do indicador "Processando..." para ações matemáticas e de
#       interface. O aviso é desenhado por blitting quando possível antes da
#       atualização e ocultado antes do redraw final.
# =============================================================================


from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.widgets import Button, Slider, TextBox


# =============================================================================
# 1. PATCH DEFENSIVO PARA EVENTOS DO MATPLOTLIB
# =============================================================================
# Em algumas combinações recentes de Python/Matplotlib/backend gráfico, eventos
# de redimensionamento da janela podem chegar a wrappers internos de widgets que
# esperam atributos típicos de eventos de mouse, como event.inaxes, event.x e
# event.y. ResizeEvent normalmente não possui esses atributos.
#
# O patch abaixo adiciona valores neutros aos eventos que não possuem esses
# atributos e ignora AttributeError específico de ResizeEvent. Isso não altera
# eventos normais de mouse.

_PROCESS_CALLBACKS_ORIGINAL = plt.matplotlib.cbook.CallbackRegistry.process


def _process_callbacks_evento_seguro(self, sinal, *args, **kwargs):
    """Torna widgets mais tolerantes a ResizeEvent em backends problemáticos."""
    if args:
        evento = args[0]

        for nome, valor in (
            ("inaxes", None),
            ("x", -1),
            ("y", -1),
            ("xdata", None),
            ("ydata", None),
            ("button", None),
            ("key", None),
            ("step", 0),
        ):
            if not hasattr(evento, nome):
                try:
                    setattr(evento, nome, valor)
                except Exception:
                    pass

    try:
        return _PROCESS_CALLBACKS_ORIGINAL(self, sinal, *args, **kwargs)
    except AttributeError:
        if args and type(args[0]).__name__ == "ResizeEvent":
            return
        raise


plt.matplotlib.cbook.CallbackRegistry.process = _process_callbacks_evento_seguro


# =============================================================================
# 2. CONFIGURAÇÃO DIDÁTICA
# =============================================================================

# -----------------------------------------------------------------------------
# 2.1 Onda quadrada e discretização temporal
# -----------------------------------------------------------------------------

AMPLITUDE_PICO_V = 1.0
NUM_PERIODOS_VISIVEIS = 4
AMOSTRAS_POR_PERIODO = 2500


# -----------------------------------------------------------------------------
# 2.2 Número de harmônicos
# -----------------------------------------------------------------------------

N_MIN = 1
N_MAX = 200
N_MAX_SLIDER = 15
N_INICIAL = 2

# O cálculo de Fourier pode usar M até N_MAX. Porém, o slider visual vai até
# N_MAX_SLIDER para aumentar a resolução de pixels na região didaticamente mais
# usada. Valores acima de N_MAX_SLIDER ainda podem ser digitados na caixa M.
#
# Desenhar 200 senoides individuais
# no gráfico temporal é caro e pouco legível. Este limite afeta somente a
# visualização dos harmônicos individuais no primeiro gráfico.
MAX_HARMONICOS_INDIVIDUAIS_DESENHADOS = 40


# -----------------------------------------------------------------------------
# 2.3 Frequências preparadas para a atividade
# -----------------------------------------------------------------------------

# Frequências preparadas para o circuito R = 1 kΩ, C = 0.47 µF.
# As frequências do segundo circuito são calculadas automaticamente de modo
# a preservar aproximadamente as mesmas razões f0/fc.
FREQUENCIAS_1K_HZ = (72.0, 360.0, 7.2e3)
ROTULOS_REGIME = ("baixo", "≈ corte", "alto")


# -----------------------------------------------------------------------------
# 2.4 Estado inicial dos elementos exibidos
# -----------------------------------------------------------------------------

MOSTRAR_FOURIER_INICIAL = True
MOSTRAR_SAIDA_AJUSTADA_INICIAL = True
MOSTRAR_HARMONICOS_INDIVIDUAIS_INICIAL = False
MOSTRAR_RETAS_FIT_INICIAL = True
MOSTRAR_ESPECTRO_FIT_INICIAL = True
USAR_FASE_RC_AJUSTE_INICIAL = False


# -----------------------------------------------------------------------------
# 2.5 Escala visual
# -----------------------------------------------------------------------------

ESCALA_INTERFACE_INICIAL = 1.00
ESCALA_INTERFACE_MIN = 0.50
ESCALA_INTERFACE_MAX = 3.00
PASSO_ESCALA_INTERFACE = 0.25


# -----------------------------------------------------------------------------
# 2.6 Constantes numéricas auxiliares
# -----------------------------------------------------------------------------

EPS_GANHO = 1.0e-6
ESPECTRO_Y_MIN = 1.0e-5
ESPECTRO_Y_MAX = 1.5




# =============================================================================
# 2.x CONFIGURAÇÃO DE PROFILING / DIAGNÓSTICO DE DESEMPENHO
# =============================================================================
# Esta versão de teste imprime no terminal o tempo gasto em cada etapa relevante
# quando o usuário mexe na interface.
#
# A meta é separar:
#     1. tempo de cálculo físico/matemático;
#     2. tempo de atualização de dados dos artistas do Matplotlib;
#     3. tempo até o evento real de redesenho da figura.
#
# Para desativar os prints, mude DEBUG_PERFORMANCE para False.

DEBUG_PERFORMANCE = False

# Só imprime etapas acima deste limiar. Use 0.0 para imprimir tudo.
PERF_PRINT_THRESHOLD_MS = 0.0

# Se True, substitui draw_idle() por draw() em algumas chamadas, medindo o tempo
# bloqueante de renderização. Deixe False para reproduzir o comportamento normal
# da interface. Use True apenas em testes pontuais.
PERF_FORCAR_DRAW_SINCRONO = False


# =============================================================================
# 3. JANELA INICIAL DE ESCALA VISUAL
# =============================================================================

def solicitar_escala_interface_inicial() -> float:
    """
    Abre uma janela pequena para o usuário escolher a escala visual inicial.

    A janela principal do Matplotlib só é criada depois que a escala é definida.
    Isso evita que a aplicação precise redimensionar widgets, fontes, legendas
    e marcadores durante o uso.

    Retorna
    -------
    float
        Escala visual interna do programa. Exemplo: 1.0 para 100%.
    """
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        return ESCALA_INTERFACE_INICIAL

    def limitar_escala(valor: float) -> float:
        return float(np.clip(valor, ESCALA_INTERFACE_MIN, ESCALA_INTERFACE_MAX))

    def texto_para_escala(texto: str) -> float | None:
        try:
            valor = float(texto.strip().replace("%", "").replace(",", "."))
        except ValueError:
            return None

        # Aceita tanto "125" quanto "1.25".
        if valor > 10:
            valor = valor / 100.0

        return limitar_escala(valor)

    escala_atual = {"valor": ESCALA_INTERFACE_INICIAL}

    root = tk.Tk()
    root.title("Escala visual do programa")
    root.resizable(False, False)

    try:
        root.attributes("-topmost", True)
        root.after(300, lambda: root.attributes("-topmost", False))
    except Exception:
        pass

    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")

    titulo = ttk.Label(
        frame,
        text="Escolha a escala visual inicial",
        font=("Segoe UI", 11, "bold"),
    )
    titulo.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 8))

    explicacao = ttk.Label(
        frame,
        text=(
            "Essa escala controla fontes, legendas, botões e marcadores da interface.\n"
            "Ela será aplicada uma única vez, antes da abertura da janela principal."
        ),
        justify="left",
    )
    explicacao.grid(row=1, column=0, columnspan=5, sticky="w", pady=(0, 10))

    ttk.Label(frame, text="Escala do programa:").grid(
        row=2,
        column=0,
        sticky="w",
        padx=(0, 8),
    )

    escala_var = tk.StringVar(value=f"{int(round(100 * escala_atual['valor']))}")

    entrada = ttk.Entry(frame, width=8, textvariable=escala_var, justify="center")
    entrada.grid(row=2, column=1, sticky="w")

    ttk.Label(frame, text="%").grid(row=2, column=2, sticky="w", padx=(3, 8))

    def aplicar_delta(delta: float) -> None:
        valor = texto_para_escala(escala_var.get())

        if valor is None:
            valor = escala_atual["valor"]

        valor = limitar_escala(valor + delta)
        escala_atual["valor"] = valor
        escala_var.set(f"{int(round(100 * valor))}")

    ttk.Button(
        frame,
        text="−",
        width=4,
        command=lambda: aplicar_delta(-PASSO_ESCALA_INTERFACE),
    ).grid(row=2, column=3, sticky="w", padx=(0, 4))

    ttk.Button(
        frame,
        text="+",
        width=4,
        command=lambda: aplicar_delta(+PASSO_ESCALA_INTERFACE),
    ).grid(row=2, column=4, sticky="w")

    recomendacao = ttk.Label(
        frame,
        text=(
            "Sugestões iniciais:\n"
            "• FHD/1920×1080 ou 1920×1200 com escala do sistema 100%: 100%.\n"
            "• FHD com escala do sistema 125–150%: 75–100%.\n"
            "• 4K/3840×2160 com escala do sistema 100%: 150–200%.\n"
            "• 4K com escala do sistema 150–200%: 100–150%.\n\n"
            "Termo geral: escala de exibição ou escala do sistema.\n"
            "Windows: Escala. Ubuntu/GNOME: Scale / Fractional Scaling."
        ),
        justify="left",
    )
    recomendacao.grid(row=3, column=0, columnspan=5, sticky="w", pady=(12, 10))

    aviso = ttk.Label(
        frame,
        text=(
            f"Intervalo permitido: {int(100 * ESCALA_INTERFACE_MIN)}% "
            f"a {int(100 * ESCALA_INTERFACE_MAX)}%. "
            f"Botões: passos de {int(100 * PASSO_ESCALA_INTERFACE)}%."
        ),
        foreground="#555555",
    )
    aviso.grid(row=4, column=0, columnspan=5, sticky="w", pady=(0, 10))

    resultado = {"escala": ESCALA_INTERFACE_INICIAL}

    def confirmar() -> None:
        valor = texto_para_escala(escala_var.get())

        if valor is None:
            valor = escala_atual["valor"]

        resultado["escala"] = limitar_escala(valor)
        root.destroy()

    def cancelar() -> None:
        resultado["escala"] = ESCALA_INTERFACE_INICIAL
        root.destroy()

    def usar_100() -> None:
        escala_var.set("100")
        confirmar()

    botoes = ttk.Frame(frame)
    botoes.grid(row=5, column=0, columnspan=5, sticky="e")

    ttk.Button(botoes, text="Usar 100%", command=usar_100).grid(row=0, column=0, padx=(0, 6))
    ttk.Button(botoes, text="Cancelar", command=cancelar).grid(row=0, column=1, padx=(0, 6))
    ttk.Button(botoes, text="Abrir programa", command=confirmar).grid(row=0, column=2)

    entrada.focus_set()
    entrada.selection_range(0, tk.END)

    root.bind("<Return>", lambda _event: confirmar())
    root.bind("<Escape>", lambda _event: cancelar())
    root.protocol("WM_DELETE_WINDOW", cancelar)

    root.update_idletasks()

    largura = root.winfo_width()
    altura = root.winfo_height()
    x = int((root.winfo_screenwidth() - largura) / 2)
    y = int((root.winfo_screenheight() - altura) / 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

    return resultado["escala"]


# =============================================================================
# 4. TEMA VISUAL ESTÁTICO
# =============================================================================

def limitar_escala_interface(escala: float) -> float:
    """
    Limita a escala visual ao intervalo permitido.
    """
    return float(np.clip(escala, ESCALA_INTERFACE_MIN, ESCALA_INTERFACE_MAX))


def criar_tema_visual(escala: float) -> dict[str, float | tuple[float, float]]:
    """
    Cria um dicionário com todos os valores visuais usados pela interface.

    Esta função deve ser chamada uma única vez, antes da construção da janela
    principal. Depois disso, as funções de update usam valores já prontos e não
    ficam multiplicando nem reaplicando escala durante o uso.

    Parâmetros
    ----------
    escala : float
        Escala visual interna do programa.

    Retorna
    -------
    dict
        Dicionário de tamanhos, larguras, fontes e marcadores.
    """
    escala = limitar_escala_interface(escala)

    # A figura em si cresce pouco com a escala. O usuário ainda pode maximizar
    # a janela pelo sistema operacional. Crescer demais a janela automaticamente
    # pode fazê-la nascer maior que a tela em alguns notebooks.
    escala_figura = min(max(escala, 1.0), 1.35)

    return {
        # Figura
        "fig_largura": 15.8 * escala_figura,
        "fig_altura": 8.8 * escala_figura,

        # Fontes dos gráficos
        "fonte_titulo": 12.5 * escala,
        "fonte_eixo": 10.0 * escala,
        "fonte_tick": 8.5 * escala,
        "fonte_legenda": 7.6 * escala,

        # Fontes do painel
        "fonte_painel_titulo": 13.0 * escala,
        "fonte_painel_grupo": 9.5 * escala,
        "fonte_painel": 8.5 * escala,
        "fonte_painel_pequena": 7.4 * escala,
        "fonte_monospace": 8.6 * escala,

        # Linhas e marcadores
        "linha_principal": 1.6 * escala,
        "linha_secundaria": 1.1 * escala,
        "linha_fourier": 1.2 * escala,
        "linha_saida_fourier": 1.7 * escala,
        "linha_harmonico": 0.60 * escala,
        "marcador": 3.8 * escala,
        "spine": 0.8 * escala,

        # Harmônicos individuais
        "alpha_harmonicos": 0.24,

        # Posições fixas da figura
        "subplots_left": 0.065,
        "subplots_right": 0.975,
        "subplots_top": 0.925,
        "subplots_bottom": 0.08,
        "subplots_wspace": 0.24,
        "subplots_hspace": 0.34,
    }


# =============================================================================
# 5. SLIDER NÃO LINEAR PARA O NÚMERO DE HARMÔNICOS
# =============================================================================

VALORES_M_SLIDER = np.array(
    list(range(N_MIN, N_MAX_SLIDER + 1, 1)),
    dtype=int,
)

VALORES_M_SLIDER = np.array(
    sorted(set(int(v) for v in VALORES_M_SLIDER if N_MIN <= v <= N_MAX_SLIDER)),
    dtype=int,
)

if VALORES_M_SLIDER[0] != N_MIN:
    VALORES_M_SLIDER = np.insert(VALORES_M_SLIDER, 0, N_MIN)

if VALORES_M_SLIDER[-1] != N_MAX_SLIDER:
    VALORES_M_SLIDER = np.append(VALORES_M_SLIDER, N_MAX_SLIDER)


def indice_slider_para_m(valor_slider: float) -> int:
    """
    Converte a posição interna do slider no número físico de harmônicos.
    """
    indice = int(np.clip(round(valor_slider), 0, len(VALORES_M_SLIDER) - 1))
    return int(VALORES_M_SLIDER[indice])


def m_para_indice_slider(m_harmonicos: int) -> int:
    """
    Retorna o índice do valor permitido mais próximo de m_harmonicos.
    """
    diferencas = np.abs(VALORES_M_SLIDER - int(m_harmonicos))
    return int(np.argmin(diferencas))


def proximo_m_na_escala_nao_linear(m_atual: int, direcao: int) -> int:
    """
    Retorna o próximo valor de M na escala discreta não linear.

    direcao = +1 avança; direcao = -1 retrocede.
    """
    valores = VALORES_M_SLIDER
    m_atual = int(m_atual)

    if direcao > 0:
        candidatos = valores[valores > m_atual]
        if len(candidatos) == 0:
            return int(valores[-1])
        return int(candidatos[0])

    candidatos = valores[valores < m_atual]

    if len(candidatos) == 0:
        return int(N_MIN)

    return int(candidatos[-1])


# =============================================================================
# 6. FUNÇÕES FÍSICAS E MATEMÁTICAS
# =============================================================================

@dataclass(frozen=True)
class CircuitoRC:
    """
    Representa um circuito RC série observado na tensão do capacitor.
    """

    rotulo: str
    resistencia_ohm: float
    capacitancia_f: float

    @property
    def tau_s(self) -> float:
        """
        Tempo característico τ = RC, em segundos.
        """
        return self.resistencia_ohm * self.capacitancia_f

    @property
    def fc_hz(self) -> float:
        """
        Frequência de corte fc = 1/(2πRC), em Hz.
        """
        return 1.0 / (2.0 * np.pi * self.tau_s)


CIRCUITOS_DISPONIVEIS: dict[str, CircuitoRC] = {
    "1 kΩ": CircuitoRC("1 kΩ", resistencia_ohm=1.0e3, capacitancia_f=0.47e-6),
    "47 Ω": CircuitoRC("47 Ω", resistencia_ohm=47.0, capacitancia_f=47.0e-6),
}


FC_REFERENCIA_HZ = CIRCUITOS_DISPONIVEIS["1 kΩ"].fc_hz
RAZOES_F0_SOBRE_FC = tuple(f / FC_REFERENCIA_HZ for f in FREQUENCIAS_1K_HZ)

FREQUENCIAS_POR_RESISTOR_HZ: dict[str, tuple[float, float, float]] = {
    "1 kΩ": FREQUENCIAS_1K_HZ,
    "47 Ω": tuple(r * CIRCUITOS_DISPONIVEIS["47 Ω"].fc_hz for r in RAZOES_F0_SOBRE_FC),
}


# -----------------------------------------------------------------------------
# 6.1 Formatação de grandezas
# -----------------------------------------------------------------------------

def formatar_frequencia(frequencia_hz: float) -> str:
    """
    Formata frequências com unidades convenientes.
    """
    if frequencia_hz >= 1.0e6:
        return f"{frequencia_hz / 1.0e6:.3g} MHz"
    if frequencia_hz >= 1.0e3:
        return f"{frequencia_hz / 1.0e3:.3g} kHz"
    return f"{frequencia_hz:.3g} Hz"


def formatar_tempo(tempo_s: float) -> str:
    """
    Formata tempos com unidades convenientes.
    """
    if tempo_s >= 1.0:
        return f"{tempo_s:.3g} s"
    if tempo_s >= 1.0e-3:
        return f"{tempo_s * 1.0e3:.3g} ms"
    if tempo_s >= 1.0e-6:
        return f"{tempo_s * 1.0e6:.3g} µs"
    return f"{tempo_s * 1.0e9:.3g} ns"


def rotulos_frequencias_para_resistor(rotulo_resistor: str) -> tuple[str, str, str]:
    """
    Cria rótulos legíveis para as três frequências preparadas.
    """
    return tuple(
        f"{ROTULOS_REGIME[i]}: {formatar_frequencia(f)}"
        for i, f in enumerate(FREQUENCIAS_POR_RESISTOR_HZ[rotulo_resistor])
    )


# -----------------------------------------------------------------------------
# 6.2 Fourier da onda quadrada
# -----------------------------------------------------------------------------

def indices_harmonicos_impares(m_harmonicos: int) -> np.ndarray:
    """
    Retorna os índices dos harmônicos ímpares presentes na série.

    Para M harmônicos, retorna:

        1, 3, 5, ..., 2M - 1.
    """
    m = int(np.clip(round(m_harmonicos), N_MIN, N_MAX))
    return 2 * np.arange(1, m + 1) - 1


def criar_malha_temporal(f0_hz: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Cria a malha temporal em segundos e em milissegundos.
    """
    periodo_s = 1.0 / f0_hz
    n_pontos = int(NUM_PERIODOS_VISIVEIS * AMOSTRAS_POR_PERIODO)

    t_min = -0.5 * NUM_PERIODOS_VISIVEIS * periodo_s
    t_max = +0.5 * NUM_PERIODOS_VISIVEIS * periodo_s

    tempo_s = np.linspace(t_min, t_max, n_pontos)

    return tempo_s, tempo_s * 1.0e3


def onda_quadrada_ideal(tempo_s: np.ndarray, f0_hz: float) -> np.ndarray:
    """
    Calcula a onda quadrada ideal de entrada.
    """
    return AMPLITUDE_PICO_V * np.sign(np.sin(2.0 * np.pi * f0_hz * tempo_s))


def serie_fourier_entrada(
    tempo_s: np.ndarray,
    f0_hz: float,
    m_harmonicos: int,
) -> np.ndarray:
    """
    Calcula a soma parcial da série de Fourier da onda quadrada de entrada.
    """
    indices = indices_harmonicos_impares(m_harmonicos)

    omega0 = 2.0 * np.pi * f0_hz
    fases = np.outer(indices, omega0 * tempo_s)

    coeficientes = (4.0 * AMPLITUDE_PICO_V / np.pi) / indices

    return coeficientes @ np.sin(fases)


def harmonicos_individuais_entrada(
    tempo_s: np.ndarray,
    f0_hz: float,
    m_harmonicos: int,
) -> np.ndarray:
    """
    Calcula os harmônicos individuais da entrada em forma matricial.

    Retorna
    -------
    np.ndarray
        Matriz com formato (m_harmonicos, len(tempo_s)).
    """
    indices = indices_harmonicos_impares(m_harmonicos)

    omega0 = 2.0 * np.pi * f0_hz
    fases = np.outer(indices, omega0 * tempo_s)

    coeficientes = (4.0 * AMPLITUDE_PICO_V / np.pi) / indices

    return coeficientes[:, None] * np.sin(fases)


def amplitudes_fourier_entrada(m_harmonicos: int) -> np.ndarray:
    """
    Calcula as amplitudes dos harmônicos da onda quadrada antes do filtro.
    """
    indices = indices_harmonicos_impares(m_harmonicos)
    return (4.0 * AMPLITUDE_PICO_V / np.pi) / indices


# -----------------------------------------------------------------------------
# 6.3 Resposta temporal do capacitor
# -----------------------------------------------------------------------------

def resposta_capacitor_por_trechos(
    tempo_s: np.ndarray,
    f0_hz: float,
    circuito: CircuitoRC,
) -> np.ndarray:
    """
    Solução periódica exata para onda quadrada ideal de ciclo 50%.
    """
    periodo_s = 1.0 / f0_hz
    meio_periodo_s = 0.5 * periodo_s
    tau_s = circuito.tau_s
    amplitude = AMPLITUDE_PICO_V

    alpha = np.exp(-meio_periodo_s / tau_s)

    v_inicio_positivo = -amplitude * (1.0 - alpha) / (1.0 + alpha)
    v_inicio_negativo = +amplitude * (1.0 - alpha) / (1.0 + alpha)

    fase_periodo = np.mod(tempo_s, periodo_s)
    mascara_positiva = fase_periodo < meio_periodo_s

    vc = np.empty_like(tempo_s)

    tempo_local_pos = fase_periodo[mascara_positiva]
    vc[mascara_positiva] = (
        amplitude
        + (v_inicio_positivo - amplitude) * np.exp(-tempo_local_pos / tau_s)
    )

    tempo_local_neg = fase_periodo[~mascara_positiva] - meio_periodo_s
    vc[~mascara_positiva] = (
        -amplitude
        + (v_inicio_negativo + amplitude) * np.exp(-tempo_local_neg / tau_s)
    )

    return vc


# -----------------------------------------------------------------------------
# 6.4 Resposta em frequência do filtro RC
# -----------------------------------------------------------------------------

def transferencia_rc_capacitor(
    frequencias_hz: np.ndarray | float,
    circuito: CircuitoRC,
) -> np.ndarray:
    """
    Função de transferência complexa do passa-baixa RC medido no capacitor.
    """
    frequencias = np.asarray(frequencias_hz, dtype=float)
    omega_tau = 2.0 * np.pi * frequencias * circuito.tau_s

    return 1.0 / (1.0 + 1j * omega_tau)


def ganho_rc_ideal(frequencias_hz: np.ndarray | float, circuito: CircuitoRC) -> np.ndarray:
    """
    Módulo da função de transferência RC ideal.
    """
    return np.abs(transferencia_rc_capacitor(frequencias_hz, circuito))


def serie_fourier_saida_rc(
    tempo_s: np.ndarray,
    f0_hz: float,
    m_harmonicos: int,
    circuito: CircuitoRC,
) -> np.ndarray:
    """
    Calcula a saída no capacitor por decomposição de Fourier.
    """
    indices = indices_harmonicos_impares(m_harmonicos)

    _ = circuito

    frequencias = indices * f0_hz
    omega0 = 2.0 * np.pi * f0_hz
    fases_temporais = np.outer(indices, omega0 * tempo_s)

    coeficientes = (4.0 * AMPLITUDE_PICO_V / np.pi) / indices

    h = transferencia_rc_capacitor(frequencias, circuito)
    ganhos = np.abs(h)
    fases_rc = np.angle(h)

    return (coeficientes * ganhos) @ np.sin(fases_temporais + fases_rc[:, None])


def serie_fourier_saida_ganho_ajustado(
    tempo_s: np.ndarray,
    f0_hz: float,
    m_harmonicos: int,
    circuito: CircuitoRC,
    a1: float,
    b1: float,
    a2: float,
    b2: float,
    usar_fase_rc_ideal: bool = False,
) -> np.ndarray:
    """
    Calcula a reconstrução temporal usando o ganho ajustado pelo aluno.

    As retas ajustadas em log-log fornecem apenas o módulo do ganho:

        G_fit(f) = |V_C/V_e|.

    A fase é configurável:

        usar_fase_rc_ideal = False:
            aplica apenas o módulo G_fit(f_k). Se a1=b1=a2=b2=0, então
            G_fit(f)=1 e a curva vermelha coincide com a Fourier da entrada.

        usar_fase_rc_ideal = True:
            aplica o módulo G_fit(f_k), mas usa a fase ideal do circuito RC
            para cada harmônico. Isso aproxima a defasagem temporal esperada
            de um passa-baixa RC, embora a medição do aluno tenha fornecido
            apenas o módulo do ganho.
    """
    indices = indices_harmonicos_impares(m_harmonicos)

    frequencias = indices * f0_hz
    omega0 = 2.0 * np.pi * f0_hz
    fases_temporais = np.outer(indices, omega0 * tempo_s)

    coeficientes = (4.0 * AMPLITUDE_PICO_V / np.pi) / indices
    ganhos_fit = ganho_loglog_por_retas(frequencias, a1, b1, a2, b2)

    if usar_fase_rc_ideal:
        fases_rc_ideal = np.angle(transferencia_rc_capacitor(frequencias, circuito))
        fases_temporais = fases_temporais + fases_rc_ideal[:, None]

    return (coeficientes * ganhos_fit) @ np.sin(fases_temporais)


# -----------------------------------------------------------------------------
# 6.5 Retas ajustadas em escala log-log
# -----------------------------------------------------------------------------

def ganho_loglog_por_retas(
    frequencias_hz: np.ndarray | float,
    a1: float,
    b1: float,
    a2: float,
    b2: float,
) -> np.ndarray:
    """
    Calcula o ganho aproximado a partir de duas retas em escala log-log.
    """
    frequencias = np.maximum(np.asarray(frequencias_hz, dtype=float), 1.0e-300)

    logf = np.log10(frequencias)
    logg1 = a1 * logf + b1
    logg2 = a2 * logf + b2
    logg = np.minimum(logg1, logg2)

    return np.clip(10.0 ** logg, EPS_GANHO, 1.0)


def intersecao_retas_loglog(
    a1: float,
    b1: float,
    a2: float,
    b2: float,
) -> float | None:
    """
    Calcula a frequência de interseção das duas retas log-log.
    """
    denominador = a1 - a2

    if np.isclose(denominador, 0.0):
        return None

    logf = (b2 - b1) / denominador
    f = 10.0 ** logf

    if not np.isfinite(f) or f <= 0.0:
        return None

    return float(f)


def coeficientes_retas_padrao(circuito: CircuitoRC) -> tuple[float, float, float, float]:
    """
    Retas assintóticas padrão para o ganho do capacitor.

    Baixa frequência:
        G ≈ 1  -> log10(G) = 0.

    Alta frequência:
        G ≈ fc/f -> log10(G) = -log10(f) + log10(fc).
    """
    return 0.0, 0.0, -1.0, np.log10(circuito.fc_hz)


# =============================================================================
# 7. APLICAÇÃO INTERATIVA
# =============================================================================

class AplicacaoOndaQuadradaRC:
    """
    Aplicação interativa Matplotlib para o estudo de Fourier + filtro RC.
    """

    def __init__(self, escala_inicial: float = ESCALA_INTERFACE_INICIAL) -> None:
        # ---------------------------------------------------------------------
        # Tema visual estático
        # ---------------------------------------------------------------------
        self.escala_interface = limitar_escala_interface(escala_inicial)
        self.tema = criar_tema_visual(self.escala_interface)

        # ---------------------------------------------------------------------
        # Estado físico inicial
        # ---------------------------------------------------------------------
        self.rotulo_resistor = "1 kΩ"
        self.indice_frequencia = 1
        self.circuito = CIRCUITOS_DISPONIVEIS[self.rotulo_resistor]

        self.f0_hz = FREQUENCIAS_POR_RESISTOR_HZ[self.rotulo_resistor][
            self.indice_frequencia
        ]

        self.m_harmonicos = N_INICIAL

        # ---------------------------------------------------------------------
        # Estado de visibilidade
        # ---------------------------------------------------------------------
        self.mostrar_fourier = MOSTRAR_FOURIER_INICIAL
        self.mostrar_saida_ajustada = MOSTRAR_SAIDA_AJUSTADA_INICIAL
        self.mostrar_harmonicos_individuais = MOSTRAR_HARMONICOS_INDIVIDUAIS_INICIAL
        self.mostrar_retas_fit = MOSTRAR_RETAS_FIT_INICIAL
        self.mostrar_espectro_fit = MOSTRAR_ESPECTRO_FIT_INICIAL
        self.usar_fase_rc_ajuste = USAR_FASE_RC_AJUSTE_INICIAL

        # ---------------------------------------------------------------------
        # Retas log-log iniciais
        # ---------------------------------------------------------------------
        self.a1, self.b1, self.a2, self.b2 = coeficientes_retas_padrao(self.circuito)

        # ---------------------------------------------------------------------
        # Malhas numéricas
        # ---------------------------------------------------------------------
        self.tempo_s, self.tempo_ms = criar_malha_temporal(self.f0_hz)
        self.frequencias_plot_hz = self._criar_malha_frequencias()

        # ---------------------------------------------------------------------
        # Controle contra loops entre slider e caixa de texto
        # ---------------------------------------------------------------------
        self._sincronizando_widgets = False

        # ---------------------------------------------------------------------
        # Controle do modo commit do slider de M
        # ---------------------------------------------------------------------
        # O Matplotlib redesenha a figura inteira quando um Slider faz draw_idle().
        # Como cada redraw completo está na escala de ~0,2 s no Windows/backend
        # atual, o slider não deve recalcular os gráficos a cada movimento do
        # mouse. Em vez disso:
        #
        #     - durante o arraste: guardamos apenas o M pendente;
        #     - ao soltar o botão do mouse: aplicamos o M uma única vez.
        #
        # Também deixamos slider_m.drawon = False após a criação do widget para
        # evitar redraws intermediários do próprio slider durante o arraste.
        self._slider_m_em_arraste = False
        self._slider_m_pendente = self.m_harmonicos
        self._textbox_m_ultimo_texto_confirmado = str(self.m_harmonicos)

        # Background usado para redesenhar somente o eixo do slider durante
        # o arraste. O valor é atualizado depois de cada redraw completo.
        self._slider_m_background = None

        # Background usado pelo indicador "Processando...". Quando o backend
        # suporta blitting, o aviso é desenhado rapidamente sem forçar redraw
        # completo da figura antes do cálculo/interface.
        self._processando_background = None
        self._processando_visivel = False

        # ---------------------------------------------------------------------
        # Figura e eixos
        # ---------------------------------------------------------------------
        self.fig = plt.figure(
            figsize=(self.tema["fig_largura"], self.tema["fig_altura"])
        )

        # Layout em duas linhas para telas 16:9:
        #
        #     linha superior: configurações | ganho + espectro
        #     linha inferior: tensão no tempo ocupando toda a largura
        #
        # O espectro harmônico usa o eixo direito do gráfico de ganho.
        grade = self.fig.add_gridspec(
            2,
            2,
            height_ratios=[1.00, 1.25],
            width_ratios=[1.05, 1.45],
            left=0.045,
            right=0.985,
            top=0.895,
            bottom=0.085,
            wspace=0.22,
            hspace=0.34,
        )

        self.ax_painel = self.fig.add_subplot(grade[0, 0])
        self.ax_ganho = self.fig.add_subplot(grade[0, 1])
        self.ax_tempo = self.fig.add_subplot(grade[1, :])
        self.ax_espectro = self.ax_ganho.twinx()

        self.ax_painel.axis("off")

        self.texto_processando = self.fig.text(
            0.985,
            0.965,
            "Processando...",
            ha="right",
            va="top",
            fontsize=0.92 * self.tema["fonte_painel_grupo"],
            fontweight="bold",
            color="white",
            bbox={
                "boxstyle": "round,pad=0.35",
                "facecolor": "tab:red",
                "edgecolor": "none",
                "alpha": 0.88,
            },
            visible=False,
            zorder=5000,
        )

        self._criar_grafico_temporal()
        self._criar_grafico_ganho()
        self._criar_grafico_espectro()
        self._criar_painel_configuracao()
        self._conectar_widgets()
        self.fig.canvas.mpl_connect("draw_event", self._evento_draw)

        # Aplica estilos de seleção uma única vez.
        self._atualizar_estilos_controles()

        # Primeiro preenchimento de dados.
        self._atualizar_tudo(redesenhar=False)


    # -------------------------------------------------------------------------
    def _perf_inicio(self, nome_acao: str) -> None:
        """
        Inicia medição de uma ação de interface.

        Exemplo de ação:
            - mudança de M pelo slider;
            - digitação de M;
            - troca de frequência;
            - troca de resistor;
            - alteração das retas.
        """
        if not DEBUG_PERFORMANCE:
            return

        agora = time.perf_counter()
        self._perf_acao = nome_acao
        self._perf_t0 = agora
        self._perf_t_ultimo = agora

        print("\n" + "=" * 78)
        print(f"[PERF] AÇÃO: {nome_acao}")
        print("=" * 78)

    # -------------------------------------------------------------------------
    def _perf_marca(self, etapa: str) -> None:
        """
        Imprime o tempo desde a última marca e desde o início da ação.
        """
        if not DEBUG_PERFORMANCE:
            return

        agora = time.perf_counter()
        delta_ms = 1000.0 * (agora - self._perf_t_ultimo)
        total_ms = 1000.0 * (agora - self._perf_t0)

        self._perf_t_ultimo = agora

        if delta_ms >= PERF_PRINT_THRESHOLD_MS:
            print(f"[PERF]   {etapa:<48} {delta_ms:9.3f} ms   total {total_ms:9.3f} ms")

    # -------------------------------------------------------------------------
    def _perf_fim(self, etapa: str = "fim da ação") -> None:
        """
        Finaliza a medição de uma ação.
        """
        if not DEBUG_PERFORMANCE:
            return

        agora = time.perf_counter()
        total_ms = 1000.0 * (agora - self._perf_t0)

        print(f"[PERF]   {etapa:<48} {'':>9}      total {total_ms:9.3f} ms")
        print("=" * 78)

    # -------------------------------------------------------------------------
    def _solicitar_redesenho(self, origem: str) -> None:
        """
        Agenda o redesenho da figura e mede o tempo até o draw_event.

        draw_idle() agenda o redesenho sem bloquear a função de callback.
        Esta função NÃO pode chamar a si mesma. Na v17 havia uma recursão
        acidental aqui, que gerava RecursionError e contaminava os tempos.
        """
        if DEBUG_PERFORMANCE:
            self._draw_pendente = {
                "origem": origem,
                "t0": time.perf_counter(),
            }

        self._ocultar_processando_sem_redraw()

        if PERF_FORCAR_DRAW_SINCRONO:
            t0 = time.perf_counter()
            self.fig.canvas.draw()

            if DEBUG_PERFORMANCE:
                dt_ms = 1000.0 * (time.perf_counter() - t0)
                print(f"[PERF]   draw() síncrono [{origem}]                 {dt_ms:9.3f} ms")
        else:
            self.fig.canvas.draw_idle()

    # -------------------------------------------------------------------------
    def _evento_draw(self, _evento) -> None:
        """
        Callback chamado pelo Matplotlib após renderização da figura.

        Além do profiling opcional, este callback atualiza os backgrounds usados
        para blitting:
            - slider de M;
            - indicador "Processando...".
        """
        self._cachear_background_slider_m()
        self._cachear_background_processando()
        self._redesenhar_slider_m_leve()

        if not DEBUG_PERFORMANCE:
            return

        pendente = getattr(self, "_draw_pendente", None)

        if not pendente:
            return

        dt_ms = 1000.0 * (time.perf_counter() - pendente["t0"])

        print(f"[PERF] DRAW EVENT [{pendente['origem']}] {'':<30} {dt_ms:9.3f} ms após solicitação")

        self._draw_pendente = None


    # -------------------------------------------------------------------------
    def _cachear_background_processando(self) -> None:
        """
        Armazena o fundo da figura para desenhar o aviso "Processando..." por blit.

        O fundo é capturado com o texto invisível, logo depois de um redraw
        completo. Assim, o aviso pode ser ligado e desligado sem redesenhar toda
        a figura antes da atualização.
        """
        if not hasattr(self, "texto_processando"):
            return

        canvas = self.fig.canvas

        if not getattr(canvas, "supports_blit", False):
            self._processando_background = None
            return

        try:
            self._processando_background = canvas.copy_from_bbox(self.fig.bbox)
        except Exception:
            self._processando_background = None

    # -------------------------------------------------------------------------
    def _mostrar_processando(self, mensagem: str = "Processando...") -> None:
        """
        Mostra um aviso visual antes de atualizações matemáticas ou de interface.

        Observação
        ----------
        Matplotlib roda essencialmente em uma única thread de interface. Por isso,
        se o backend não suportar blitting, pode ser necessário aguardar o loop
        gráfico para o aviso aparecer. Quando há suporte a blit, o aviso é
        desenhado imediatamente sem redraw completo.
        """
        if not hasattr(self, "texto_processando"):
            return

        self._processando_visivel = True
        self.texto_processando.set_text(mensagem)
        self.texto_processando.set_visible(True)

        canvas = self.fig.canvas

        if getattr(canvas, "supports_blit", False):
            if self._processando_background is None:
                self._cachear_background_processando()

            if self._processando_background is not None:
                try:
                    canvas.restore_region(self._processando_background)
                    self.fig.draw_artist(self.texto_processando)
                    canvas.blit(self.fig.bbox)
                    canvas.flush_events()
                    return
                except Exception:
                    self._processando_background = None

        # Fallback sem blit: agenda e libera o loop de eventos. Não é tão
        # garantido quanto draw() síncrono, mas evita dobrar o custo de redraw.
        try:
            canvas.draw_idle()
            canvas.flush_events()
            plt.pause(0.001)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    def _ocultar_processando_sem_redraw(self) -> None:
        """
        Oculta o aviso antes do redraw final.

        O redraw final chamado por _solicitar_redesenho() já redesenhará a
        figura sem o aviso. Assim evitamos um redraw extra apenas para apagar
        "Processando...".
        """
        if not hasattr(self, "texto_processando"):
            return

        self._processando_visivel = False
        self.texto_processando.set_visible(False)


    # -------------------------------------------------------------------------
    def _artistas_slider_m_animados(self) -> list:
        """
        Retorna os artistas do slider que mudam durante o arraste.

        Esses artistas são tratados como animados para que possam ser desenhados
        por blitting sem obrigar a figura inteira a ser redesenhada.
        """
        artistas = []

        for nome in ("poly", "_handle", "vline"):
            artista = getattr(self.slider_m, nome, None)

            if artista is None:
                continue

            if isinstance(artista, (list, tuple)):
                artistas.extend(a for a in artista if a is not None)
            else:
                artistas.append(artista)

        return artistas

    # -------------------------------------------------------------------------
    def _configurar_slider_m_para_blit(self) -> None:
        """
        Configura os artistas variáveis do slider para blitting.

        A ideia é:
            - impedir que o slider peça redraw completo durante o arraste;
            - atualizar apenas os artistas do próprio slider no pequeno eixo
              onde ele está desenhado.
        """
        for artista in self._artistas_slider_m_animados():
            try:
                artista.set_animated(True)
            except Exception:
                pass

    # -------------------------------------------------------------------------
    def _cachear_background_slider_m(self) -> None:
        """
        Armazena o fundo do eixo do slider para uso com blitting.
        """
        if not hasattr(self, "slider_m"):
            return

        canvas = self.fig.canvas

        if not getattr(canvas, "supports_blit", False):
            self._slider_m_background = None
            return

        try:
            self._slider_m_background = canvas.copy_from_bbox(self.slider_m.ax.bbox)
        except Exception:
            self._slider_m_background = None

    # -------------------------------------------------------------------------
    def _redesenhar_slider_m_leve(self) -> None:
        """
        Redesenha apenas o eixo do slider de M usando blitting.

        Se o backend não suportar blitting, a função falha silenciosamente.
        Nesse caso, o slider ainda funcionará em modo commit, mas a parte visual
        pode atualizar apenas no próximo redraw completo.
        """
        if not hasattr(self, "slider_m"):
            return

        canvas = self.fig.canvas

        if not getattr(canvas, "supports_blit", False):
            return

        if self._slider_m_background is None:
            self._cachear_background_slider_m()

        if self._slider_m_background is None:
            return

        try:
            canvas.restore_region(self._slider_m_background)

            for artista in self._artistas_slider_m_animados():
                if hasattr(artista, "get_visible") and not artista.get_visible():
                    continue

                self.slider_m.ax.draw_artist(artista)

            canvas.blit(self.slider_m.ax.bbox)
            canvas.flush_events()

        except Exception:
            # Se o backend não aceitar algum detalhe do blit, mantemos o
            # funcionamento lógico do programa e apenas abrimos mão da animação
            # leve do slider.
            self._slider_m_background = None


    # -------------------------------------------------------------------------
    def _criar_malha_frequencias(self) -> np.ndarray:
        """
        Cria a malha de frequências usada nos gráficos logarítmicos.
        """
        maior_harmonico = (2 * N_MAX - 1) * self.f0_hz

        f_min = max(1.0e-2, min(self.f0_hz, self.circuito.fc_hz) / 30.0)
        f_max = max(maior_harmonico, self.circuito.fc_hz) * 3.0

        return np.logspace(np.log10(f_min), np.log10(f_max), 1200)

    # -------------------------------------------------------------------------
    def _criar_grafico_temporal(self) -> None:
        """
        Cria as curvas do gráfico temporal.
        """
        t = self.tema

        (self.linha_entrada,) = self.ax_tempo.plot(
            [],
            [],
            linewidth=t["linha_principal"],
            zorder=5,
            label="Entrada: onda quadrada",
        )

        (self.linha_capacitor_trechos,) = self.ax_tempo.plot(
            [],
            [],
            color="tab:orange",
            alpha=0.50,
            linewidth=t["linha_principal"],
            linestyle="-",
            zorder=4,
            label="Saída ideal RC: carga/descarga",
        )

        (self.linha_entrada_fourier,) = self.ax_tempo.plot(
            [],
            [],
            color="tab:green",
            alpha=0.45,
            linewidth=t["linha_fourier"],
            linestyle="--",
            zorder=5,
            label="Entrada por Fourier",
        )

        (self.linha_saida_fourier,) = self.ax_tempo.plot(
            [],
            [],
            color="tab:red",
            alpha=0.95,
            linewidth=t["linha_saida_fourier"],
            linestyle="-",
            zorder=7,
            label="Saída por Fourier + ganho ajustado",
        )

        # Harmônicos individuais: desenhados como uma única coleção, mais leve
        # do que dezenas de Line2D independentes.
        self.colecao_harmonicos = LineCollection(
            [],
            linewidths=t["linha_harmonico"],
            alpha=t["alpha_harmonicos"],
            zorder=1,
        )

        self.ax_tempo.add_collection(self.colecao_harmonicos)

        self.proxy_harmonicos = Line2D(
            [],
            [],
            color="gray",
            linewidth=t["linha_harmonico"],
            alpha=t["alpha_harmonicos"],
            label=f"Harmônicos individuais (até {MAX_HARMONICOS_INDIVIDUAIS_DESENHADOS})",
        )

        self.texto_parametros = self.ax_tempo.text(
            0.015,
            0.03,
            "",
            transform=self.ax_tempo.transAxes,
            fontsize=t["fonte_monospace"],
            va="bottom",
            ha="left",
            family="monospace",
            bbox={"boxstyle": "round", "alpha": 0.15},
        )

        self.ax_tempo.set_xlabel("Tempo (ms)", fontsize=t["fonte_eixo"])
        self.ax_tempo.set_ylabel("Tensão normalizada", fontsize=t["fonte_eixo"])
        self.ax_tempo.set_ylim(-1.35 * AMPLITUDE_PICO_V, 1.35 * AMPLITUDE_PICO_V)
        self.ax_tempo.grid(True, linestyle="--", alpha=0.35)
        self.ax_tempo.tick_params(labelsize=t["fonte_tick"])

        self.ax_tempo.set_title(
            "Tensão no capacitor: ideal RC e ajuste harmônico",
            fontsize=t["fonte_titulo"],
        )

        handles, labels = self.ax_tempo.get_legend_handles_labels()
        handles.append(self.proxy_harmonicos)
        labels.append(self.proxy_harmonicos.get_label())

        self.legenda_tempo = self.ax_tempo.legend(
            handles,
            labels,
            loc="upper right",
            fontsize=t["fonte_legenda"],
        )

    # -------------------------------------------------------------------------
    def _criar_grafico_ganho(self) -> None:
        """
        Cria o gráfico de ganho em frequência.
        """
        t = self.tema

        (self.linha_ganho_rc,) = self.ax_ganho.loglog(
            [],
            [],
            color="0.35",
            alpha=0.38,
            linewidth=1.15 * self.escala_interface,
            linestyle="-",
            label="RC ideal: referência",
        )

        (self.linha_ganho_fit,) = self.ax_ganho.loglog(
            [],
            [],
            color="tab:red",
            alpha=0.95,
            linewidth=2.55 * self.escala_interface,
            linestyle="-",
            label="Ganho do aluno: retas inseridas",
        )

        (self.pontos_harmonicos_rc,) = self.ax_ganho.loglog(
            [],
            [],
            "o",
            color="0.35",
            alpha=0.30,
            markersize=0.75 * t["marcador"],
            label=r"$G_{RC}(f_k)$ ref.",
        )

        (self.pontos_harmonicos_fit,) = self.ax_ganho.loglog(
            [],
            [],
            "s",
            color="tab:red",
            alpha=0.95,
            markersize=1.05 * t["marcador"],
            label=r"$G_{aluno}(f_k)$ usado na curva vermelha",
        )

        self.linha_fc = self.ax_ganho.axvline(
            1.0,
            color="0.35",
            alpha=0.45,
            linestyle=":",
            linewidth=t["linha_secundaria"],
            label=r"$f_c$ ideal",
        )

        self.linha_intersecao = self.ax_ganho.axvline(
            1.0,
            color="tab:red",
            alpha=0.55,
            linestyle="-.",
            linewidth=t["linha_secundaria"],
            label="interseção das retas do aluno",
        )

        self.ax_ganho.set_xlabel("Frequência f (Hz)", fontsize=t["fonte_eixo"])
        self.ax_ganho.set_ylabel("Ganho linear G", fontsize=t["fonte_eixo"])
        self.ax_ganho.set_ylim(1.0e-3, 1.2)
        self.ax_ganho.grid(True, which="both", linestyle="--", alpha=0.35)
        self.ax_ganho.tick_params(labelsize=t["fonte_tick"])

        self.ax_ganho.set_title(
            "Ganho definido pelo aluno e referência RC",
            fontsize=t["fonte_titulo"],
        )

        self.legenda_ganho = self.ax_ganho.legend(
            loc="lower left",
            fontsize=t["fonte_legenda"],
        )

    # -------------------------------------------------------------------------
    def _criar_grafico_espectro(self) -> None:
        """
        Cria o espectro harmônico no eixo direito do gráfico de ganho.
        """
        t = self.tema

        self.ax_espectro.set_yscale("log")
        self.ax_espectro.set_ylabel("Amplitude harmônica", fontsize=t["fonte_eixo"])
        self.ax_espectro.tick_params(labelsize=t["fonte_tick"])

        (self.pontos_amp_entrada,) = self.ax_espectro.loglog(
            [],
            [],
            "o",
            color="tab:green",
            markersize=0.75 * t["marcador"],
            alpha=0.35,
            label="Amp. entrada",
        )

        (self.pontos_amp_saida_rc,) = self.ax_espectro.loglog(
            [],
            [],
            "o",
            color="0.35",
            markersize=0.75 * t["marcador"],
            alpha=0.25,
            label="Amp. ideal RC",
        )

        (self.pontos_amp_saida_fit,) = self.ax_espectro.loglog(
            [],
            [],
            "s",
            color="tab:red",
            markersize=0.95 * t["marcador"],
            alpha=0.90,
            label="Amp. aluno",
        )

        self.ax_espectro.set_ylim(ESPECTRO_Y_MIN, ESPECTRO_Y_MAX)

        self.legenda_espectro = self.ax_espectro.legend(
            loc="upper right",
            fontsize=t["fonte_legenda"],
            title="Espectro",
            title_fontsize=t["fonte_legenda"],
        )

    # -------------------------------------------------------------------------
    def _painel_axes(self, x: float, y: float, w: float, h: float):
        """
        Cria um eixo em coordenadas relativas ao quadrante de configuração.
        """
        bbox = self.ax_painel.get_position()

        return self.fig.add_axes([
            bbox.x0 + x * bbox.width,
            bbox.y0 + y * bbox.height,
            w * bbox.width,
            h * bbox.height,
        ])

    # -------------------------------------------------------------------------
    def _criar_painel_configuracao(self) -> None:
        """
        Cria widgets de configuração no painel superior esquerdo.

        Organização visual desta versão
        --------------------------------
        O painel usa uma grade manual rígida. A motivação é evitar que textos,
        botões e caixas de entrada dependam de ajustes "no olho".

        Estratégia de alinhamento:
            - cada grupo de botões tem x, largura e centro definidos por
              constantes locais;
            - títulos dos grupos ficam no centro geométrico dos botões;
            - o controle de M ocupa uma faixa própria;
            - o bloco "Ganho do aluno" é separado em título, fórmula e tabela
              de parâmetros;
            - as caixas numéricas usam texto centralizado;
            - os botões "Fase RC" e "Retas do RC ideal" ficam em uma coluna
              dedicada à direita dos parâmetros das retas.
        """
        t = self.tema

        # ------------------------------------------------------------------
        # Constantes de grade do painel
        # ------------------------------------------------------------------
        x_r, w_r = 0.06, 0.18
        x_f0, w_f0 = 0.315, 0.23
        x_exibir, w_exibir = 0.625, 0.31

        cx_r = x_r + 0.5 * w_r
        cx_f0 = x_f0 + 0.5 * w_f0
        cx_exibir = x_exibir + 0.5 * w_exibir

        h_botao = 0.060

        self.ax_painel.set_title(
            "Configurações",
            fontsize=0.92 * t["fonte_painel_titulo"],
            pad=8,
        )

        # ------------------------------------------------------------------
        # Faixa 1 — títulos dos grupos principais
        # ------------------------------------------------------------------
        self.text_titulo_r = self.ax_painel.text(
            cx_r,
            0.925,
            "R",
            transform=self.ax_painel.transAxes,
            fontsize=t["fonte_painel_grupo"],
            ha="center",
            va="center",
        )

        self.text_titulo_f0 = self.ax_painel.text(
            cx_f0,
            0.925,
            "f0 de interesse",
            transform=self.ax_painel.transAxes,
            fontsize=t["fonte_painel_grupo"],
            ha="center",
            va="center",
        )

        self.text_titulo_exibir = self.ax_painel.text(
            cx_exibir,
            0.925,
            "Exibir",
            transform=self.ax_painel.transAxes,
            fontsize=t["fonte_painel_grupo"],
            ha="center",
            va="center",
        )

        # ------------------------------------------------------------------
        # Faixa 2 — seleção de circuito, frequência e camadas exibidas
        # ------------------------------------------------------------------
        self.botao_r_1k = Button(self._painel_axes(x_r, 0.802, w_r, 0.070), "1 kΩ")
        self.botao_r_47 = Button(self._painel_axes(x_r, 0.718, w_r, 0.070), "47 Ω")

        rotulos_f0 = rotulos_frequencias_para_resistor(self.rotulo_resistor)

        self.botao_f0_baixo = Button(
            self._painel_axes(x_f0, 0.812, w_f0, h_botao),
            rotulos_f0[0],
        )

        self.botao_f0_corte = Button(
            self._painel_axes(x_f0, 0.738, w_f0, h_botao),
            rotulos_f0[1],
        )

        self.botao_f0_alto = Button(
            self._painel_axes(x_f0, 0.664, w_f0, h_botao),
            rotulos_f0[2],
        )

        self.botao_exibir_fourier = Button(
            self._painel_axes(x_exibir, 0.828, w_exibir, 0.048),
            "Fourier entrada",
        )

        self.botao_exibir_saida_ajustada = Button(
            self._painel_axes(x_exibir, 0.770, w_exibir, 0.048),
            "Saída fit",
        )

        self.botao_exibir_harmonicos = Button(
            self._painel_axes(x_exibir, 0.712, w_exibir, 0.048),
            "Harmônicos",
        )

        self.botao_exibir_retas = Button(
            self._painel_axes(x_exibir, 0.654, w_exibir, 0.048),
            "Retas",
        )

        self.botao_exibir_espectro_fit = Button(
            self._painel_axes(x_exibir, 0.596, w_exibir, 0.048),
            "Espectro",
        )

        # ------------------------------------------------------------------
        # Faixa 3 — resumo físico
        # ------------------------------------------------------------------
        ax_resumo = self._painel_axes(0.055, 0.505, 0.89, 0.112)
        ax_resumo.axis("off")

        self.texto_resumo_painel = ax_resumo.text(
            0.0,
            0.98,
            "",
            transform=ax_resumo.transAxes,
            va="top",
            ha="left",
            fontsize=0.95 * t["fonte_monospace"],
            family="monospace",
        )

        # ------------------------------------------------------------------
        # Faixa 4 — controle de M
        # ------------------------------------------------------------------
        ax_slider = self._painel_axes(0.095, 0.415, 0.515, 0.040)

        self.slider_m = Slider(
            ax=ax_slider,
            label="M harmônicos",
            valmin=0,
            valmax=len(VALORES_M_SLIDER) - 1,
            valinit=m_para_indice_slider(self.m_harmonicos),
            valstep=1,
        )

        # Desativa redraw automático do slider. A figura inteira será
        # redesenhada apenas quando o valor for efetivamente confirmado.
        # Durante o arraste, redesenhamos somente o eixo do slider via blitting.
        self.slider_m.drawon = False

        self._configurar_slider_m_para_blit()

        self.slider_m.label.set_fontsize(0.88 * t["fonte_painel"])

        # Oculta o valor numérico nativo do Slider para eliminar a sobreposição
        # com a TextBox de M. O valor confirmado aparece na caixa M.
        self.slider_m.valtext.set_visible(False)
        self.slider_m.valtext.set_fontsize(t["fonte_painel"])
        self.slider_m.valtext.set_text(f"M = {self.m_harmonicos}")

        ax_m = self._painel_axes(0.715, 0.393, 0.120, 0.058)
        self.text_m = TextBox(ax_m, "M", initial=str(self.m_harmonicos))

        if hasattr(self.text_m, "cursor"):
            self.text_m.cursor.set_visible(False)

        self.text_m.label.set_fontsize(t["fonte_painel"])
        self.text_m.text_disp.set_fontsize(t["fonte_painel"])

        self.botao_m_menos = Button(
            self._painel_axes(0.855, 0.394, 0.055, 0.056),
            "−",
        )

        self.botao_m_mais = Button(
            self._painel_axes(0.915, 0.394, 0.055, 0.056),
            "+",
        )

        ax_m_info = self._painel_axes(0.095, 0.360, 0.86, 0.034)
        ax_m_info.axis("off")

        self.texto_info_m = ax_m_info.text(
            0.0,
            0.5,
            "Slider/botões: M até 15; caixa M até 200.",
            fontsize=t["fonte_painel_pequena"],
            va="center",
        )

        # ------------------------------------------------------------------
        # Faixa 5 — título e fórmula do ganho do aluno
        # ------------------------------------------------------------------
        self.ax_label_ganho_aluno = self._painel_axes(0.060, 0.304, 0.88, 0.032)
        self.ax_label_ganho_aluno.axis("off")

        self.texto_eq_retas = self.ax_label_ganho_aluno.text(
            0.0,
            0.50,
            "Ganho do aluno → curva vermelha",
            fontsize=0.70 * t["fonte_painel_grupo"],
            fontweight="bold",
            color="tab:red",
            va="center",
            ha="left",
        )

        self.ax_formula_ganho_aluno = self._painel_axes(0.060, 0.272, 0.88, 0.026)
        self.ax_formula_ganho_aluno.axis("off")

        self.texto_eq_retas_formula = self.ax_formula_ganho_aluno.text(
            0.0,
            0.50,
            "log10(G)=a log10(f)+b   |   envelope: menor das duas retas",
            fontsize=0.76 * t["fonte_painel_pequena"],
            va="center",
            ha="left",
        )

        # ------------------------------------------------------------------
        # Faixa 6 — tabela de parâmetros das retas
        # ------------------------------------------------------------------
        self.ax_label_reta1 = self._painel_axes(0.060, 0.225, 0.215, 0.035)
        self.ax_label_reta1.axis("off")
        self.ax_label_reta1.text(
            0.0,
            0.5,
            "Reta 1: platô",
            fontsize=t["fonte_painel_pequena"],
            fontweight="bold",
            va="center",
            ha="left",
        )

        self.text_a1 = TextBox(
            self._painel_axes(0.315, 0.214, 0.125, 0.052),
            "a1",
            initial=f"{self.a1:.6g}",
        )

        self.text_b1 = TextBox(
            self._painel_axes(0.535, 0.214, 0.125, 0.052),
            "b1",
            initial=f"{self.b1:.6g}",
        )

        self.ax_label_reta2 = self._painel_axes(0.060, 0.158, 0.215, 0.035)
        self.ax_label_reta2.axis("off")
        self.ax_label_reta2.text(
            0.0,
            0.5,
            "Reta 2: queda",
            fontsize=t["fonte_painel_pequena"],
            fontweight="bold",
            va="center",
            ha="left",
        )

        self.text_a2 = TextBox(
            self._painel_axes(0.315, 0.147, 0.125, 0.052),
            "a2",
            initial=f"{self.a2:.6g}",
        )

        self.text_b2 = TextBox(
            self._painel_axes(0.535, 0.147, 0.125, 0.052),
            "b2",
            initial=f"{self.b2:.6g}",
        )

        for caixa in (self.text_m, self.text_a1, self.text_b1, self.text_a2, self.text_b2):
            caixa.label.set_fontsize(t["fonte_painel"])
            caixa.text_disp.set_fontsize(t["fonte_painel"])
            caixa.text_disp.set_ha("center")
            caixa.text_disp.set_position((0.5, 0.5))

        self.botao_fase_rc = Button(
            self._painel_axes(0.735, 0.214, 0.205, 0.052),
            "Fase RC: OFF",
        )

        self.botao_reset = Button(
            self._painel_axes(0.735, 0.147, 0.205, 0.052),
            "Retas do RC ideal",
        )

        # ------------------------------------------------------------------
        # Faixa 7 — dica final
        # ------------------------------------------------------------------
        self.texto_dica_db = self.ax_painel.text(
            0.060,
            0.064,
            "dB: a=A/20, b=B/20    |    a=b=0 e fase OFF → vermelho = Fourier",
            transform=self.ax_painel.transAxes,
            fontsize=0.90 * t["fonte_painel_pequena"],
            ha="left",
            va="center",
        )

        # ------------------------------------------------------------------
        # Fontes dos botões
        # ------------------------------------------------------------------
        for botao in (
            self.botao_r_1k,
            self.botao_r_47,
            self.botao_f0_baixo,
            self.botao_f0_corte,
            self.botao_f0_alto,
            self.botao_exibir_fourier,
            self.botao_exibir_saida_ajustada,
            self.botao_exibir_harmonicos,
            self.botao_exibir_retas,
            self.botao_exibir_espectro_fit,
            self.botao_m_menos,
            self.botao_m_mais,
            self.botao_fase_rc,
            self.botao_reset,
        ):
            botao.label.set_fontsize(t["fonte_painel"])

    # -------------------------------------------------------------------------
    def _conectar_widgets(self) -> None:
        """
        Conecta widgets a seus respectivos callbacks.
        """
        self.botao_r_1k.on_clicked(lambda _e: self._selecionar_resistor("1 kΩ"))
        self.botao_r_47.on_clicked(lambda _e: self._selecionar_resistor("47 Ω"))

        self.botao_f0_baixo.on_clicked(lambda _e: self._selecionar_frequencia(0))
        self.botao_f0_corte.on_clicked(lambda _e: self._selecionar_frequencia(1))
        self.botao_f0_alto.on_clicked(lambda _e: self._selecionar_frequencia(2))

        self.botao_exibir_fourier.on_clicked(lambda _e: self._alternar_visibilidade("fourier"))
        self.botao_exibir_saida_ajustada.on_clicked(lambda _e: self._alternar_visibilidade("saida_ajustada"))
        self.botao_exibir_harmonicos.on_clicked(lambda _e: self._alternar_visibilidade("harmonicos"))
        self.botao_exibir_retas.on_clicked(lambda _e: self._alternar_visibilidade("retas"))
        self.botao_exibir_espectro_fit.on_clicked(lambda _e: self._alternar_visibilidade("espectro_fit"))

        self.slider_m.on_changed(self._evento_slider_m)
        self.text_m.on_submit(self._evento_texto_m)

        # Eventos globais:
        #     - button_press_event detecta início de arraste do slider e também
        #       confirma a caixa M quando o usuário clica fora dela.
        #     - button_release_event aplica o valor do slider uma única vez.
        self.fig.canvas.mpl_connect("button_press_event", self._evento_mouse_press)
        self.fig.canvas.mpl_connect("button_release_event", self._evento_mouse_release)

        self.botao_m_menos.on_clicked(lambda _e: self._alterar_m_por_botao(-1))
        self.botao_m_mais.on_clicked(lambda _e: self._alterar_m_por_botao(+1))

        for caixa in (self.text_a1, self.text_b1, self.text_a2, self.text_b2):
            caixa.on_submit(self._evento_textbox_retas)

        self.botao_fase_rc.on_clicked(lambda _e: self._alternar_visibilidade("fase_rc"))
        self.botao_reset.on_clicked(lambda _e: self._resetar_retas_para_circuito_atual())

    # -------------------------------------------------------------------------
    def _estilizar_botao_estado(self, botao: Button, ativo: bool) -> None:
        """
        Aplica estilo visual simples de ligado/desligado ou selecionado.
        """
        cor_ativo = "#b7e1ff"
        cor_inativo = "#f0f0f0"

        botao.ax.set_facecolor(cor_ativo if ativo else cor_inativo)
        botao.color = cor_ativo if ativo else cor_inativo
        botao.hovercolor = "#d9ecff" if ativo else "#e8e8e8"
        botao.label.set_fontweight("bold" if ativo else "normal")

    # -------------------------------------------------------------------------
    def _atualizar_estilos_controles(self) -> None:
        """
        Atualiza realce visual dos botões de seleção e alternância.
        """
        self._estilizar_botao_estado(self.botao_r_1k, self.rotulo_resistor == "1 kΩ")
        self._estilizar_botao_estado(self.botao_r_47, self.rotulo_resistor == "47 Ω")

        for i, botao in enumerate((self.botao_f0_baixo, self.botao_f0_corte, self.botao_f0_alto)):
            self._estilizar_botao_estado(botao, self.indice_frequencia == i)

        self._estilizar_botao_estado(self.botao_exibir_fourier, self.mostrar_fourier)
        self._estilizar_botao_estado(self.botao_exibir_saida_ajustada, self.mostrar_saida_ajustada)
        self._estilizar_botao_estado(self.botao_exibir_harmonicos, self.mostrar_harmonicos_individuais)
        self._estilizar_botao_estado(self.botao_exibir_retas, self.mostrar_retas_fit)
        self._estilizar_botao_estado(self.botao_exibir_espectro_fit, self.mostrar_espectro_fit)
        self._estilizar_botao_estado(self.botao_fase_rc, self.usar_fase_rc_ajuste)
        self.botao_fase_rc.label.set_text("Fase RC: ON" if self.usar_fase_rc_ajuste else "Fase RC: OFF")

    # -------------------------------------------------------------------------
    def _atualizar_rotulos_frequencia(self) -> None:
        """
        Atualiza os textos dos botões de frequência.
        """
        rotulos = rotulos_frequencias_para_resistor(self.rotulo_resistor)

        for botao, rotulo in zip(
            (self.botao_f0_baixo, self.botao_f0_corte, self.botao_f0_alto),
            rotulos,
        ):
            botao.label.set_text(rotulo)

    # -------------------------------------------------------------------------
    def _set_textbox_sem_draw(self, caixa: TextBox, texto: str) -> None:
        """
        Atualiza visualmente uma TextBox sem chamar TextBox.set_val().

        Motivo
        ------
        Em Matplotlib, TextBox.set_val() chama internamente _rendercursor().
        Essa rotina pode executar fig.canvas.draw() de forma síncrona para medir
        a posição do cursor. Nos logs da v17, a sincronização slider/textbox de M
        custava cerca de 220–235 ms, enquanto o cálculo físico ficava abaixo de
        1 ms.

        Nota sobre Matplotlib
        ---------------------
        TextBox.text é uma property somente leitura que retorna
        text_disp.get_text(). Portanto, esta função atualiza apenas
        text_disp.set_text(texto). Depois disso, caixa.text já retorna o novo
        valor sem chamar TextBox.set_val().
        """
        texto = str(texto)
        eventson_original = caixa.eventson

        try:
            caixa.eventson = False
            caixa.text_disp.set_text(texto)

            if hasattr(caixa, "cursor_index"):
                caixa.cursor_index = len(texto)

            if hasattr(caixa, "cursor"):
                caixa.cursor.set_visible(False)

        finally:
            caixa.eventson = eventson_original

    # -------------------------------------------------------------------------
    def _set_slider_m_sem_evento(self) -> None:
        """
        Move o slider para o índice correspondente a M sem callback/redraw.

        Slider.set_val() normalmente chama draw_idle() quando drawon=True.
        Para mudanças vindas de botão ou caixa de texto, desligamos drawon e
        eventson temporariamente e fazemos apenas um draw_idle() ao fim da
        atualização completa.
        """
        drawon_original = self.slider_m.drawon
        eventson_original = self.slider_m.eventson

        self.slider_m.drawon = False
        self.slider_m.eventson = False

        try:
            self.slider_m.set_val(m_para_indice_slider(self.m_harmonicos))
            self.slider_m.valtext.set_text(f"M = {self.m_harmonicos}")

        finally:
            self.slider_m.eventson = eventson_original
            self.slider_m.drawon = drawon_original

    # -------------------------------------------------------------------------
    def _sincronizar_controle_m(self, origem: str = "externa") -> None:
        """
        Sincroniza slider e caixa de texto com M atual, sem draw síncrono.

        Parâmetros
        ----------
        origem : str
            - "slider": a posição do slider já mudou; não chamamos set_val().
            - "textbox": o usuário já digitou o valor; só corrigimos o texto
              se houver clipping/arredondamento.
            - "botao": precisamos mover o slider, mas sem event/draw.
        """
        self._sincronizando_widgets = True

        try:
            # TextBox.set_val() é evitado de propósito.
            self._set_textbox_sem_draw(self.text_m, str(self.m_harmonicos))
            self._textbox_m_ultimo_texto_confirmado = str(self.m_harmonicos)

            # O slider mostra o M físico real, não o índice interno do slider.
            self.slider_m.valtext.set_text(f"M = {self.m_harmonicos}")

            # Quando a origem é o próprio slider, a posição já foi atualizada
            # pelo Matplotlib. Rechamar Slider.set_val() aqui era o gargalo.
            if origem != "slider":
                self._set_slider_m_sem_evento()

        finally:
            self._sincronizando_widgets = False

    # -------------------------------------------------------------------------
    def _definir_m(self, novo_m: int, atualizar: bool = True, origem: str = "externa") -> None:
        """
        Define M e atualiza os gráficos dependentes de M.

        Parâmetros
        ----------
        novo_m : int
            Novo número de harmônicos ímpares.
        atualizar : bool
            Se True, atualiza gráficos dependentes de M.
        origem : str
            Origem da alteração: "slider_release", "textbox_enter", "clique_fora", "botao" ou "externa".
            Esse parâmetro evita sincronizações caras e redraws intermediários.
        """
        novo_m = int(np.clip(round(novo_m), N_MIN, N_MAX))

        if novo_m == self.m_harmonicos:
            return

        self._mostrar_processando("Processando M...")

        self._perf_inicio(f"alterar M: {self.m_harmonicos} -> {novo_m} | origem={origem}")

        self.m_harmonicos = novo_m
        self._perf_marca("atribuir novo M")

        origem_sync = "slider" if origem == "slider_release" else origem
        self._sincronizar_controle_m(origem=origem_sync)
        self._perf_marca("sincronizar slider/textbox de M")

        if atualizar:
            self._atualizar_por_m()
            self._perf_marca("_atualizar_por_m completo")

        self._perf_fim()

    # -------------------------------------------------------------------------
    def _evento_slider_m(self, valor_slider: float) -> None:
        """
        Callback do slider de M.

        Modo commit:
            - durante o arraste, apenas guarda o M pendente;
            - não recalcula Fourier;
            - não redesenha os gráficos;
            - ao soltar o mouse, _evento_mouse_release aplica o valor.
        """
        if self._sincronizando_widgets:
            return

        m_pendente = indice_slider_para_m(valor_slider)
        self._slider_m_pendente = m_pendente

        # A caixa M será sincronizada quando o valor for confirmado ao soltar
        # o mouse. Durante o arraste, redesenhamos apenas o controle visual.
        self.slider_m.valtext.set_text(f"M = {m_pendente}")

        # Redesenha somente o eixo do slider. Isso permite que a parte visual
        # acompanhe o mouse sem recalcular Fourier e sem redraw completo.
        self._redesenhar_slider_m_leve()

    # -------------------------------------------------------------------------
    def _evento_mouse_press(self, evento) -> None:
        """
        Processa clique global da janela.

        Funções:
            1. detectar início de arraste no slider de M;
            2. confirmar a caixa de texto M quando o usuário clica fora dela.
        """
        # Início de interação com o slider.
        if getattr(evento, "inaxes", None) is self.slider_m.ax:
            self._slider_m_em_arraste = True
            self._slider_m_pendente = indice_slider_para_m(self.slider_m.val)
            self._cachear_background_slider_m()
            return

        # Clique fora da caixa M: aplica o valor digitado, se mudou.
        if getattr(evento, "inaxes", None) is not self.text_m.ax:
            self._confirmar_textbox_m_se_necessario(origem="clique_fora")

    # -------------------------------------------------------------------------
    def _evento_mouse_release(self, evento) -> None:
        """
        Aplica o valor pendente do slider ao soltar o botão do mouse.
        """
        if not self._slider_m_em_arraste:
            return

        self._slider_m_em_arraste = False

        m_pendente = int(np.clip(self._slider_m_pendente, N_MIN, N_MAX))

        # Garante que o slider fique visualmente coerente com a posição final.
        self.slider_m.valtext.set_text(f"M = {m_pendente}")
        self._redesenhar_slider_m_leve()

        self._definir_m(m_pendente, origem="slider_release")

    # -------------------------------------------------------------------------
    def _confirmar_textbox_m_se_necessario(self, origem: str) -> None:
        """
        Aplica o valor da caixa M se ele mudou.

        Usada para permitir que a caixa de texto funcione tanto com Enter
        quanto quando o usuário clica fora dela.
        """
        texto_atual = str(getattr(self.text_m, "text", "")).strip()

        if texto_atual == self._textbox_m_ultimo_texto_confirmado:
            return

        self._evento_texto_m(texto_atual, origem=origem)

    # -------------------------------------------------------------------------
    def _evento_texto_m(self, texto: str, origem: str = "textbox_enter") -> None:
        """
        Callback da caixa de texto de M.

        A caixa aplica o valor:
            - ao pressionar Enter;
            - ao clicar fora da caixa.
        """
        try:
            novo_m = int(round(float(str(texto).replace(",", "."))))
        except ValueError:
            self._sincronizar_controle_m(origem="textbox_invalido")
            self._textbox_m_ultimo_texto_confirmado = str(self.m_harmonicos)
            return

        novo_m = int(np.clip(novo_m, N_MIN, N_MAX))
        self._textbox_m_ultimo_texto_confirmado = str(novo_m)

        self._definir_m(novo_m, origem=origem)

    # -------------------------------------------------------------------------
    def _alterar_m_por_botao(self, direcao: int) -> None:
        """
        Altera M usando a escala não linear.
        """
        self._definir_m(proximo_m_na_escala_nao_linear(self.m_harmonicos, direcao), origem="botao")

    # -------------------------------------------------------------------------
    def _selecionar_resistor(self, rotulo: str) -> None:
        """
        Seleciona o circuito RC.
        """
        if rotulo == self.rotulo_resistor:
            return

        self._mostrar_processando("Processando circuito...")

        self._perf_inicio(f"trocar resistor: {self.rotulo_resistor} -> {rotulo}")

        self.rotulo_resistor = rotulo
        self.circuito = CIRCUITOS_DISPONIVEIS[rotulo]

        self._atualizar_rotulos_frequencia()

        self.f0_hz = FREQUENCIAS_POR_RESISTOR_HZ[self.rotulo_resistor][
            self.indice_frequencia
        ]

        self.tempo_s, self.tempo_ms = criar_malha_temporal(self.f0_hz)
        self.frequencias_plot_hz = self._criar_malha_frequencias()

        self.a1, self.b1, self.a2, self.b2 = coeficientes_retas_padrao(self.circuito)
        self._sincronizar_textboxes_retas()

        self._atualizar_estilos_controles()
        self._perf_marca("resistor: atualizar estilos controles")

        self._atualizar_tudo()
        self._perf_marca("resistor: _atualizar_tudo completo")
        self._perf_fim()

    # -------------------------------------------------------------------------
    def _selecionar_frequencia(self, indice: int) -> None:
        """
        Seleciona uma das três frequências preparadas.
        """
        indice = int(np.clip(indice, 0, 2))

        if indice == self.indice_frequencia:
            return

        self._mostrar_processando("Processando frequência...")

        self._perf_inicio(f"trocar f0: índice {self.indice_frequencia} -> {indice}")

        self.indice_frequencia = indice

        self.f0_hz = FREQUENCIAS_POR_RESISTOR_HZ[self.rotulo_resistor][
            self.indice_frequencia
        ]

        self.tempo_s, self.tempo_ms = criar_malha_temporal(self.f0_hz)
        self.frequencias_plot_hz = self._criar_malha_frequencias()

        self._atualizar_estilos_controles()
        self._perf_marca("f0: atualizar estilos controles")

        self._atualizar_tudo()
        self._perf_marca("f0: _atualizar_tudo completo")
        self._perf_fim()

    # -------------------------------------------------------------------------
    def _alternar_visibilidade(self, nome: str) -> None:
        """
        Alterna um grupo de curvas visíveis.
        """
        self._mostrar_processando("Processando interface...")

        self._perf_inicio(f"alternar visibilidade: {nome}")

        if nome == "fourier":
            self.mostrar_fourier = not self.mostrar_fourier
            self._atualizar_visibilidade_fourier()

        elif nome == "saida_ajustada":
            self.mostrar_saida_ajustada = not self.mostrar_saida_ajustada
            self._atualizar_visibilidade_fourier()

        elif nome == "harmonicos":
            self.mostrar_harmonicos_individuais = not self.mostrar_harmonicos_individuais
            self._atualizar_harmonicos_individuais()

        elif nome == "retas":
            self.mostrar_retas_fit = not self.mostrar_retas_fit
            self._atualizar_visibilidade_retas()

        elif nome == "espectro_fit":
            self.mostrar_espectro_fit = not self.mostrar_espectro_fit
            self.pontos_amp_saida_fit.set_visible(self.mostrar_espectro_fit)

        elif nome == "fase_rc":
            self.usar_fase_rc_ajuste = not self.usar_fase_rc_ajuste
            self._atualizar_fourier_temporal()

        self._atualizar_estilos_controles()
        self._solicitar_redesenho("M")

    # -------------------------------------------------------------------------
    def _sincronizar_textboxes_retas(self) -> None:
        """
        Sincroniza as caixas de texto das retas com os valores internos.

        Usa atualização leve para evitar TextBox.set_val() e seus draws
        síncronos. Isso afeta principalmente reset de retas e troca de resistor.
        """
        for caixa, valor in (
            (self.text_a1, self.a1),
            (self.text_b1, self.b1),
            (self.text_a2, self.a2),
            (self.text_b2, self.b2),
        ):
            self._set_textbox_sem_draw(caixa, f"{valor:.6g}")

    # -------------------------------------------------------------------------
    def _ler_retas_das_caixas(self) -> bool:
        """
        Lê os coeficientes das retas das caixas de texto.

        Retorna
        -------
        bool
            True se a leitura foi bem-sucedida; False caso contrário.
        """
        try:
            self.a1 = float(self.text_a1.text.replace(",", "."))
            self.b1 = float(self.text_b1.text.replace(",", "."))
            self.a2 = float(self.text_a2.text.replace(",", "."))
            self.b2 = float(self.text_b2.text.replace(",", "."))

        except ValueError:
            self._sincronizar_textboxes_retas()
            return False

        return True

    # -------------------------------------------------------------------------
    def _evento_textbox_retas(self, _texto: str) -> None:
        """
        Callback para alteração dos coeficientes das retas.
        """
        self._mostrar_processando("Processando ganho...")

        self._perf_inicio("alterar retas")

        if not self._ler_retas_das_caixas():
            self._perf_marca("retas: leitura inválida")
            self._perf_fim()
            return

        self._perf_marca("retas: ler caixas")

        self._atualizar_por_retas()
        self._perf_marca("retas: _atualizar_por_retas completo")
        self._perf_fim()

    # -------------------------------------------------------------------------
    def _resetar_retas_para_circuito_atual(self) -> None:
        """
        Restaura as retas assintóticas padrão do circuito atual.
        """
        self._mostrar_processando("Processando retas...")

        self._perf_inicio("resetar retas RC")

        self.a1, self.b1, self.a2, self.b2 = coeficientes_retas_padrao(self.circuito)
        self._perf_marca("reset retas: calcular coeficientes padrão")

        self._sincronizar_textboxes_retas()
        self._perf_marca("reset retas: sincronizar caixas")

        self._atualizar_por_retas()
        self._perf_marca("reset retas: _atualizar_por_retas completo")
        self._perf_fim()

    # -------------------------------------------------------------------------
    def _atualizar_tudo(self, redesenhar: bool = True) -> None:
        """
        Atualiza todos os dados gráficos.

        Esta função não reaplica escala visual.
        """
        self._atualizar_temporal_completo()
        self._atualizar_ganho_completo()
        self._atualizar_espectro_completo()
        self._atualizar_texto_painel()
        self._atualizar_visibilidades()

        if redesenhar:
            self._solicitar_redesenho("tudo")

    # -------------------------------------------------------------------------
    def _atualizar_por_m(self) -> None:
        """
        Atualiza somente o que depende de M.
        """
        self._atualizar_fourier_temporal()
        self._perf_marca("M: atualizar curvas temporais de Fourier")

        self._atualizar_harmonicos_individuais()
        self._perf_marca("M: atualizar harmônicos individuais")

        self._atualizar_pontos_harmonicos_ganho()
        self._perf_marca("M: atualizar pontos no gráfico de ganho")

        self._atualizar_espectro_completo()
        self._perf_marca("M: atualizar espectro")

        self._atualizar_texto_painel()
        self._perf_marca("M: atualizar textos")

        self._solicitar_redesenho("M")
        self._perf_marca("M: solicitar redesenho")

    # -------------------------------------------------------------------------
    def _atualizar_por_retas(self) -> None:
        """
        Atualiza apenas elementos dependentes das retas ajustadas.
        """
        self._atualizar_fourier_temporal()
        self._atualizar_retas_ganho()
        self._atualizar_espectro_fit()
        self._atualizar_visibilidade_retas()

        self._solicitar_redesenho("retas")

    # -------------------------------------------------------------------------
    def _atualizar_temporal_completo(self) -> None:
        """
        Atualiza o gráfico temporal completo.
        """
        ve_ideal = onda_quadrada_ideal(self.tempo_s, self.f0_hz)

        vc_trechos = resposta_capacitor_por_trechos(
            self.tempo_s,
            self.f0_hz,
            self.circuito,
        )

        self.linha_entrada.set_data(self.tempo_ms, ve_ideal)
        self.linha_capacitor_trechos.set_data(self.tempo_ms, vc_trechos)

        self.ax_tempo.set_xlim(self.tempo_ms[0], self.tempo_ms[-1])

        self._atualizar_fourier_temporal()
        self._atualizar_harmonicos_individuais()

    # -------------------------------------------------------------------------
    def _atualizar_fourier_temporal(self) -> None:
        """
        Atualiza as curvas de Fourier no domínio temporal.
        """
        t0 = time.perf_counter()

        ve_fourier = serie_fourier_entrada(
            self.tempo_s,
            self.f0_hz,
            self.m_harmonicos,
        )

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     cálculo entrada Fourier                  {1000.0 * (time.perf_counter() - t0):9.3f} ms")

        t0 = time.perf_counter()

        vc_fourier = serie_fourier_saida_ganho_ajustado(
            self.tempo_s,
            self.f0_hz,
            self.m_harmonicos,
            self.circuito,
            self.a1,
            self.b1,
            self.a2,
            self.b2,
            self.usar_fase_rc_ajuste,
        )

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     cálculo saída Fourier + H_RC             {1000.0 * (time.perf_counter() - t0):9.3f} ms")

        t0 = time.perf_counter()

        self.linha_entrada_fourier.set_data(self.tempo_ms, ve_fourier)
        self.linha_saida_fourier.set_data(self.tempo_ms, vc_fourier)

        self._atualizar_visibilidade_fourier()

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     set_data Fourier temporal                {1000.0 * (time.perf_counter() - t0):9.3f} ms")

    # -------------------------------------------------------------------------
    def _atualizar_harmonicos_individuais(self) -> None:
        """
        Atualiza os harmônicos individuais no primeiro gráfico.
        """
        if not self.mostrar_harmonicos_individuais:
            t0 = time.perf_counter()
            self.colecao_harmonicos.set_segments([])
            self.colecao_harmonicos.set_visible(False)

            if DEBUG_PERFORMANCE:
                print(f"[PERF]     ocultar harmônicos individuais          {1000.0 * (time.perf_counter() - t0):9.3f} ms")

            return

        m_desenhado = min(
            self.m_harmonicos,
            MAX_HARMONICOS_INDIVIDUAIS_DESENHADOS,
        )

        t0 = time.perf_counter()

        harmonicos = harmonicos_individuais_entrada(
            self.tempo_s,
            self.f0_hz,
            m_desenhado,
        )

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     cálculo harmônicos individuais ({m_desenhado}) {1000.0 * (time.perf_counter() - t0):9.3f} ms")

        t0 = time.perf_counter()

        segmentos = [
            np.column_stack((self.tempo_ms, harmonico))
            for harmonico in harmonicos
        ]

        cores = [
            plt.cm.tab10(i % 10)
            for i in range(m_desenhado)
        ]

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     montar segmentos LineCollection          {1000.0 * (time.perf_counter() - t0):9.3f} ms")

        t0 = time.perf_counter()

        self.colecao_harmonicos.set_segments(segmentos)
        self.colecao_harmonicos.set_color(cores)
        self.colecao_harmonicos.set_visible(True)

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     set LineCollection harmônicos            {1000.0 * (time.perf_counter() - t0):9.3f} ms")

    # -------------------------------------------------------------------------
    def _atualizar_ganho_completo(self) -> None:
        """
        Atualiza o gráfico de ganho completo.
        """
        ganhos_rc = ganho_rc_ideal(self.frequencias_plot_hz, self.circuito)

        self.linha_ganho_rc.set_data(self.frequencias_plot_hz, ganhos_rc)

        self.linha_fc.set_xdata([self.circuito.fc_hz, self.circuito.fc_hz])
        self.linha_fc.set_label(rf"$f_c$ ideal = {formatar_frequencia(self.circuito.fc_hz)}")

        self.ax_ganho.set_xlim(self.frequencias_plot_hz[0], self.frequencias_plot_hz[-1])

        self._atualizar_retas_ganho()
        self._atualizar_pontos_harmonicos_ganho()

    # -------------------------------------------------------------------------
    def _atualizar_retas_ganho(self) -> None:
        """
        Atualiza o envelope das retas e a interseção.
        """
        ganhos_fit = ganho_loglog_por_retas(
            self.frequencias_plot_hz,
            self.a1,
            self.b1,
            self.a2,
            self.b2,
        )

        self.linha_ganho_fit.set_data(self.frequencias_plot_hz, ganhos_fit)

        f_intersecao = intersecao_retas_loglog(self.a1, self.b1, self.a2, self.b2)

        if f_intersecao is None:
            self.linha_intersecao.set_visible(False)
        else:
            self.linha_intersecao.set_xdata([f_intersecao, f_intersecao])
            self.linha_intersecao.set_label(
                f"interseção das retas ≈ {formatar_frequencia(f_intersecao)}"
            )
            self.linha_intersecao.set_visible(self.mostrar_retas_fit)

        self._atualizar_pontos_harmonicos_fit()

    # -------------------------------------------------------------------------
    def _atualizar_pontos_harmonicos_ganho(self) -> None:
        """
        Atualiza os pontos dos harmônicos no gráfico de ganho.
        """
        t0 = time.perf_counter()

        indices = indices_harmonicos_impares(self.m_harmonicos)
        frequencias_harmonicos = indices * self.f0_hz

        ganhos_harmonicos_rc = ganho_rc_ideal(
            frequencias_harmonicos,
            self.circuito,
        )

        self.pontos_harmonicos_rc.set_data(
            frequencias_harmonicos,
            ganhos_harmonicos_rc,
        )

        self._atualizar_pontos_harmonicos_fit()

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     atualizar pontos ganho RC/fit            {1000.0 * (time.perf_counter() - t0):9.3f} ms")

    # -------------------------------------------------------------------------
    def _atualizar_pontos_harmonicos_fit(self) -> None:
        """
        Atualiza os pontos G_fit(f_k) no gráfico de ganho.
        """
        indices = indices_harmonicos_impares(self.m_harmonicos)
        frequencias_harmonicos = indices * self.f0_hz

        ganhos_harmonicos_fit = ganho_loglog_por_retas(
            frequencias_harmonicos,
            self.a1,
            self.b1,
            self.a2,
            self.b2,
        )

        self.pontos_harmonicos_fit.set_data(
            frequencias_harmonicos,
            ganhos_harmonicos_fit,
        )

    # -------------------------------------------------------------------------
    def _atualizar_espectro_completo(self) -> None:
        """
        Atualiza o gráfico de espectro.
        """
        t0 = time.perf_counter()

        indices = indices_harmonicos_impares(self.m_harmonicos)
        frequencias = indices * self.f0_hz

        amplitudes_entrada = amplitudes_fourier_entrada(self.m_harmonicos)
        ganhos_rc = ganho_rc_ideal(frequencias, self.circuito)

        self.pontos_amp_entrada.set_data(frequencias, amplitudes_entrada)

        self.pontos_amp_saida_rc.set_data(
            frequencias,
            amplitudes_entrada * ganhos_rc,
        )

        self.ax_espectro.set_xlim(self.frequencias_plot_hz[0], self.frequencias_plot_hz[-1])
        self.ax_espectro.set_ylim(ESPECTRO_Y_MIN, ESPECTRO_Y_MAX)

        self._atualizar_espectro_fit()

        if DEBUG_PERFORMANCE:
            print(f"[PERF]     atualizar espectro completo              {1000.0 * (time.perf_counter() - t0):9.3f} ms")

    # -------------------------------------------------------------------------
    def _atualizar_espectro_fit(self) -> None:
        """
        Atualiza apenas a curva/pontos de espectro calculada pelas retas.
        """
        indices = indices_harmonicos_impares(self.m_harmonicos)
        frequencias = indices * self.f0_hz

        amplitudes_entrada = amplitudes_fourier_entrada(self.m_harmonicos)

        ganhos_fit = ganho_loglog_por_retas(
            frequencias,
            self.a1,
            self.b1,
            self.a2,
            self.b2,
        )

        self.pontos_amp_saida_fit.set_data(
            frequencias,
            amplitudes_entrada * ganhos_fit,
        )

        self.pontos_amp_saida_fit.set_visible(self.mostrar_espectro_fit)

    # -------------------------------------------------------------------------
    def _atualizar_texto_painel(self) -> None:
        """
        Atualiza textos informativos.
        """
        frequencias = FREQUENCIAS_POR_RESISTOR_HZ[self.rotulo_resistor]
        freq_baixa, freq_corte, freq_alta = frequencias

        periodo_s = 1.0 / self.f0_hz

        texto_temporal = (
            f"R = {self.rotulo_resistor}    "
            f"C = {self.circuito.capacitancia_f * 1e6:.3g} µF\n"
            f"τ = {formatar_tempo(self.circuito.tau_s)}    "
            f"fc = {formatar_frequencia(self.circuito.fc_hz)}\n"
            f"f0/fc = {self.f0_hz / self.circuito.fc_hz:.3g}    "
            f"T/(2τ) = {0.5 * periodo_s / self.circuito.tau_s:.3g}"
        )

        self.texto_parametros.set_text(texto_temporal)

        texto_painel = (
            f"C = {self.circuito.capacitancia_f * 1e6:.3g} µF    "
            f"τ = {formatar_tempo(self.circuito.tau_s)}    "
            f"fc = {formatar_frequencia(self.circuito.fc_hz)}\n"
            f"f0 atual = {formatar_frequencia(self.f0_hz)}    "
            f"f0/fc = {self.f0_hz / self.circuito.fc_hz:.3g}    "
            f"M = {self.m_harmonicos}    "
            f"fase={'RC' if self.usar_fase_rc_ajuste else 'OFF'}\n"
            f"Regimes: baixo {formatar_frequencia(freq_baixa)}, "
            f"corte {formatar_frequencia(freq_corte)}, "
            f"alto {formatar_frequencia(freq_alta)}"
        )

        self.texto_resumo_painel.set_text(texto_painel)

    # -------------------------------------------------------------------------
    def _atualizar_visibilidade_fourier(self) -> None:
        """
        Atualiza visibilidade das curvas de Fourier.
        """
        self.linha_entrada_fourier.set_visible(self.mostrar_fourier)
        self.linha_saida_fourier.set_visible(self.mostrar_saida_ajustada)

    # -------------------------------------------------------------------------
    def _atualizar_visibilidade_retas(self) -> None:
        """
        Atualiza visibilidade dos elementos associados às retas ajustadas.
        """
        self.linha_ganho_fit.set_visible(self.mostrar_retas_fit)
        self.pontos_harmonicos_fit.set_visible(self.mostrar_retas_fit)

        f_intersecao = intersecao_retas_loglog(self.a1, self.b1, self.a2, self.b2)
        self.linha_intersecao.set_visible(self.mostrar_retas_fit and f_intersecao is not None)

    # -------------------------------------------------------------------------
    def _atualizar_visibilidades(self) -> None:
        """
        Aplica todas as visibilidades atuais.
        """
        self._atualizar_visibilidade_fourier()
        self._atualizar_visibilidade_retas()
        self.pontos_amp_saida_fit.set_visible(self.mostrar_espectro_fit)

        if not self.mostrar_harmonicos_individuais:
            self.colecao_harmonicos.set_visible(False)


# =============================================================================
# 8. FUNÇÃO PRINCIPAL
# =============================================================================

def main() -> None:
    """
    Ponto de entrada do programa.

    Primeiro solicita a escala visual desejada em uma janela pequena. Depois,
    cria a aplicação principal já com essa escala travada durante a execução.
    """
    escala_inicial = solicitar_escala_interface_inicial()

    AplicacaoOndaQuadradaRC(escala_inicial=escala_inicial)

    plt.show()


# =============================================================================
# 9. PONTO DE ENTRADA DO SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()
