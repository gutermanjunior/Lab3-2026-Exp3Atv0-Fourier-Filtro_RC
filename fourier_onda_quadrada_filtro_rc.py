# =============================================================================
# Arquivo: fourier_onda_quadrada_filtro_rc.py
# Título: Onda Quadrada, Harmônicos de Fourier e Filtragem Passa-Baixa RC
#
# Descrição:
#     Este programa mostra como uma onda quadrada pode ser construída pela soma
#     parcial dos seus harmônicos ímpares de Fourier e como esses harmônicos são
#     atenuados por um filtro passa-baixa.
#
# Objetivo didático:
#     Ilustrar a sequência conceitual:
#
#         onda quadrada no tempo
#             → decomposição em harmônicos ímpares
#             → ganho do filtro em cada frequência harmônica
#             → reconstrução da onda filtrada
#
# Autor: Guterman Junior
# Data: 20260708
# Versão: 1.0
#
# Dependências:
#     numpy
#     matplotlib
#
# Execução:
#     python fourier_onda_quadrada_filtro_rc.py
#
# Modelo matemático da onda quadrada:
#     v_in(t) = (4/pi) * sum_{k=1}^{N} sin(2*pi*(2k - 1)*f0*t)/(2k - 1)
#
# Modelo da filtragem:
#     Cada harmônico da onda quadrada é multiplicado pelo ganho do filtro
#     avaliado na frequência física desse harmônico:
#
#         f_k = (2k - 1) f0
#         A_k,filtrado = A_k * G(f_k)
#
# Observação:
#     Por padrão, esta simulação aplica apenas a atenuação de amplitude.
#     A fase do filtro RC pode ser ativada na seção de configuração.
#
# Nota:
#     Código escrito para fins educacionais, priorizando clareza, organização
#     e legibilidade.
# =============================================================================


# =============================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons


# =============================================================================
# 2. ÁREA PRINCIPAL DE CONFIGURAÇÃO DIDÁTICA
# =============================================================================
# Esta é a seção que o professor ou monitor deve alterar antes da aula.
# Os alunos não precisam configurar os coeficientes de Fourier: eles são
# calculados automaticamente para a onda quadrada ímpar.


# -----------------------------------------------------------------------------
# 2.1 Configuração da onda quadrada
# -----------------------------------------------------------------------------

# Frequência fundamental da onda quadrada produzida pelo gerador de funções.
# Exemplo: f0 = 100 Hz significa que os harmônicos presentes estarão em
# 100 Hz, 300 Hz, 500 Hz, 700 Hz, ...
FREQUENCIA_FUNDAMENTAL_HZ = 100.0

# Número de períodos da onda quadrada que serão mostrados no gráfico temporal.
NUM_PERIODOS_VISIVEIS = 4

# Número de pontos usados na malha temporal.
# Uma malha mais densa representa melhor as oscilações próximas às transições.
NUM_POINTS = 5000


# -----------------------------------------------------------------------------
# 2.2 Configuração do slider de harmônicos
# -----------------------------------------------------------------------------

N_MIN = 1
N_MAX = 100
N_INICIAL = 10


# -----------------------------------------------------------------------------
# 2.3 Configuração do ganho passa-baixa
# -----------------------------------------------------------------------------
# O programa aceita dois modos para definir o ganho:
#
#     MODO_GANHO = "bode_db"
#         As duas retas são definidas em um gráfico de Bode:
#
#             G_dB(f) = a * log10(f) + b
#
#         Este é o modo mais natural para aproximações assintóticas de filtros.
#
#     MODO_GANHO = "linear"
#         As duas retas são definidas diretamente em ganho linear:
#
#             G(f) = a * f + b
#
#         Este modo é útil se os alunos construírem manualmente duas retas
#         sobre um gráfico de ganho linear entre 0 e 1.
#
# Em ambos os casos, o ganho passa-baixa aproximado é tomado como o menor valor
# entre as duas retas:
#
#     G(f) = min(reta_1, reta_2)
#
# Depois o resultado é limitado ao intervalo [0, 1], pois um filtro RC passivo
# não deve amplificar o sinal.

MODO_GANHO = "bode_db"
# MODO_GANHO = "linear"


# -----------------------------------------------------------------------------
# 2.4 Parâmetros das duas retas no modo "bode_db"
# -----------------------------------------------------------------------------
# Forma das retas:
#
#     G1_dB(f) = BODE_RETA_1_A * log10(f) + BODE_RETA_1_B
#     G2_dB(f) = BODE_RETA_2_A * log10(f) + BODE_RETA_2_B
#
# Para um passa-baixa idealizado:
#
#     reta 1: aproximadamente 0 dB antes do corte
#     reta 2: aproximadamente -20 dB/década depois do corte
#
# Se a reta 2 for escrita como:
#
#     G2_dB(f) = -20 log10(f/fc)
#
# então:
#
#     G2_dB(f) = -20 log10(f) + 20 log10(fc)

FREQUENCIA_CORTE_ESTIMADA_HZ = 338.6

BODE_RETA_1_A = 0.0
BODE_RETA_1_B = 0.0

BODE_RETA_2_A = -20.0
BODE_RETA_2_B = -BODE_RETA_2_A * np.log10(FREQUENCIA_CORTE_ESTIMADA_HZ)


# -----------------------------------------------------------------------------
# 2.5 Parâmetros das duas retas no modo "linear"
# -----------------------------------------------------------------------------
# Forma das retas:
#
#     G1(f) = LINEAR_RETA_1_A * f + LINEAR_RETA_1_B
#     G2(f) = LINEAR_RETA_2_A * f + LINEAR_RETA_2_B
#
# Exemplo didático:
#     reta 1 constante em G = 1
#     reta 2 cruza G = 1 na frequência de corte e depois cai linearmente

LINEAR_RETA_1_A = 0.0
LINEAR_RETA_1_B = 1.0

LINEAR_RETA_2_A = -1.0 / FREQUENCIA_CORTE_ESTIMADA_HZ
LINEAR_RETA_2_B = 2.0


# -----------------------------------------------------------------------------
# 2.6 Opção física avançada: fase do filtro RC
# -----------------------------------------------------------------------------
# Se False:
#     aplica apenas a atenuação de amplitude G(f_k).
#
# Se True:
#     além da atenuação, aplica a fase aproximada de um RC passa-baixa ideal:
#
#         phi(f) = -arctan(f/fc)
#
# Para uma primeira atividade qualitativa, recomenda-se deixar False.
# Para comparação mais realista com a bancada, pode-se testar True.

APLICAR_FASE_RC_IDEAL = False


# -----------------------------------------------------------------------------
# 2.7 Configuração visual
# -----------------------------------------------------------------------------

Y_MIN, Y_MAX = -1.5, 1.5

COR_REFERENCIA = "black"
COR_FOURIER = "red"
COR_FILTRADA = "blue"
COR_GANHO = "purple"
COR_HARMONICOS = "gray"

ALPHA_HARMONICOS = 0.35
LARGURA_HARMONICOS = 0.7

MOSTRAR_HARMONICOS_INICIALMENTE = False


# =============================================================================
# 3. FUNÇÕES DE VALIDAÇÃO
# =============================================================================

def validar_configuracao() -> None:
    """
    Valida os principais parâmetros definidos na área de configuração.

    A validação evita erros silenciosos, por exemplo frequência negativa,
    número inválido de harmônicos ou modo de ganho inexistente.
    """
    if FREQUENCIA_FUNDAMENTAL_HZ <= 0:
        raise ValueError("A frequência fundamental deve ser positiva.")

    if N_MIN < 1:
        raise ValueError("N_MIN deve ser maior ou igual a 1.")

    if N_MAX < N_MIN:
        raise ValueError("N_MAX deve ser maior ou igual a N_MIN.")

    if not (N_MIN <= N_INICIAL <= N_MAX):
        raise ValueError("N_INICIAL deve estar entre N_MIN e N_MAX.")

    if MODO_GANHO not in {"bode_db", "linear"}:
        raise ValueError('MODO_GANHO deve ser "bode_db" ou "linear".')


def validar_n_harmonicos(n: int) -> int:
    """
    Valida o número de harmônicos escolhido pelo usuário.

    Parâmetros
    ----------
    n : int
        Número escolhido no slider.

    Retorna
    -------
    int
        Número inteiro de harmônicos, limitado ao intervalo [N_MIN, N_MAX].
    """
    n = int(n)
    return min(max(n, N_MIN), N_MAX)


# =============================================================================
# 4. FUNÇÕES MATEMÁTICAS: FOURIER DA ONDA QUADRADA
# =============================================================================

def indices_harmonicos_impares(n_harmonicos: int) -> np.ndarray:
    """
    Retorna os índices dos harmônicos ímpares presentes na onda quadrada.

    Para N = 1:
        retorna [1]

    Para N = 2:
        retorna [1, 3]

    Para N = 3:
        retorna [1, 3, 5]

    Parâmetros
    ----------
    n_harmonicos : int
        Número de harmônicos ímpares incluídos na soma.

    Retorna
    -------
    np.ndarray
        Array com os índices 1, 3, 5, ..., 2N - 1.
    """
    n_harmonicos = validar_n_harmonicos(n_harmonicos)
    return 2 * np.arange(1, n_harmonicos + 1) - 1


def frequencias_harmonicos(
    frequencia_fundamental_hz: float,
    n_harmonicos: int,
) -> np.ndarray:
    """
    Calcula as frequências físicas dos harmônicos ímpares.

    A onda quadrada ideal contém apenas harmônicos ímpares. Portanto,
    se a frequência fundamental é f0, as frequências presentes são:

        f1 = 1 f0
        f3 = 3 f0
        f5 = 5 f0
        ...

    Parâmetros
    ----------
    frequencia_fundamental_hz : float
        Frequência fundamental da onda quadrada, em Hz.
    n_harmonicos : int
        Número de harmônicos ímpares incluídos.

    Retorna
    -------
    np.ndarray
        Frequências dos harmônicos, em Hz.
    """
    indices = indices_harmonicos_impares(n_harmonicos)
    return indices * frequencia_fundamental_hz


def amplitudes_fourier_onda_quadrada(n_harmonicos: int) -> np.ndarray:
    """
    Calcula as amplitudes dos harmônicos da onda quadrada ímpar.

    Para a onda quadrada de amplitude ideal entre -1 e +1:

        A_k = (4/pi) / (2k - 1)

    Parâmetros
    ----------
    n_harmonicos : int
        Número de harmônicos ímpares incluídos.

    Retorna
    -------
    np.ndarray
        Amplitudes dos harmônicos antes do filtro.
    """
    indices = indices_harmonicos_impares(n_harmonicos)
    return (4 / np.pi) / indices


def onda_quadrada_referencia(
    tempo_s: np.ndarray,
    frequencia_fundamental_hz: float,
) -> np.ndarray:
    """
    Calcula a onda quadrada ideal de referência.

    A função sign(sin(2*pi*f0*t)) representa uma onda quadrada ímpar.
    Nos pontos de descontinuidade, o valor retornado é zero, compatível
    com o valor médio dos limites laterais da série de Fourier.

    Parâmetros
    ----------
    tempo_s : np.ndarray
        Malha temporal, em segundos.
    frequencia_fundamental_hz : float
        Frequência fundamental, em Hz.

    Retorna
    -------
    np.ndarray
        Valores da onda quadrada ideal.
    """
    argumento = 2 * np.pi * frequencia_fundamental_hz * tempo_s
    return np.sign(np.sin(argumento))


def serie_fourier_onda_quadrada(
    tempo_s: np.ndarray,
    frequencia_fundamental_hz: float,
    n_harmonicos: int,
) -> np.ndarray:
    """
    Calcula a soma parcial da série de Fourier da onda quadrada.

    A soma usa automaticamente apenas harmônicos ímpares:

        v_N(t) = (4/pi) sum sin(2*pi*(2k - 1)*f0*t)/(2k - 1)

    Parâmetros
    ----------
    tempo_s : np.ndarray
        Malha temporal, em segundos.
    frequencia_fundamental_hz : float
        Frequência fundamental da onda quadrada, em Hz.
    n_harmonicos : int
        Número de harmônicos ímpares incluídos.

    Retorna
    -------
    np.ndarray
        Soma parcial da onda quadrada antes do filtro.
    """
    indices = indices_harmonicos_impares(n_harmonicos)

    soma = np.zeros_like(tempo_s)

    for indice in indices:
        frequencia_hz = indice * frequencia_fundamental_hz
        argumento = 2 * np.pi * frequencia_hz * tempo_s
        soma += np.sin(argumento) / indice

    return (4 / np.pi) * soma


def harmonicos_individuais(
    tempo_s: np.ndarray,
    frequencia_fundamental_hz: float,
    n_harmonicos: int,
) -> list[np.ndarray]:
    """
    Calcula os harmônicos individuais da onda quadrada antes do filtro.

    Esta função é usada apenas para visualização didática. A soma desses
    harmônicos reproduz a aproximação de Fourier antes da filtragem.

    Parâmetros
    ----------
    tempo_s : np.ndarray
        Malha temporal, em segundos.
    frequencia_fundamental_hz : float
        Frequência fundamental, em Hz.
    n_harmonicos : int
        Número de harmônicos calculados.

    Retorna
    -------
    list[np.ndarray]
        Lista com cada contribuição harmônica.
    """
    indices = indices_harmonicos_impares(n_harmonicos)
    harmonicos = []

    for indice in indices:
        frequencia_hz = indice * frequencia_fundamental_hz
        argumento = 2 * np.pi * frequencia_hz * tempo_s
        y = (4 / np.pi) * np.sin(argumento) / indice
        harmonicos.append(y)

    return harmonicos


# =============================================================================
# 5. FUNÇÕES MATEMÁTICAS: GANHO PASSA-BAIXA
# =============================================================================

def frequencia_de_intersecao_das_retas() -> float | None:
    """
    Calcula a frequência de interseção das duas retas usadas no modelo de ganho.

    No modo "bode_db", resolve:

        a1 log10(f) + b1 = a2 log10(f) + b2

    No modo "linear", resolve:

        a1 f + b1 = a2 f + b2

    Retorna
    -------
    float | None
        Frequência de interseção em Hz, ou None se as retas forem paralelas
        ou se o resultado não for fisicamente válido.
    """
    if MODO_GANHO == "bode_db":
        denominador = BODE_RETA_1_A - BODE_RETA_2_A

        if np.isclose(denominador, 0.0):
            return None

        log10_f = (BODE_RETA_2_B - BODE_RETA_1_B) / denominador
        frequencia_hz = 10 ** log10_f

    else:
        denominador = LINEAR_RETA_1_A - LINEAR_RETA_2_A

        if np.isclose(denominador, 0.0):
            return None

        frequencia_hz = (LINEAR_RETA_2_B - LINEAR_RETA_1_B) / denominador

    if frequencia_hz <= 0 or not np.isfinite(frequencia_hz):
        return None

    return float(frequencia_hz)


def ganho_passa_baixa(frequencias_hz: np.ndarray | float) -> np.ndarray:
    """
    Calcula o ganho linear do filtro passa-baixa nas frequências fornecidas.

    O ganho é construído a partir de duas retas. A menor delas define a
    envoltória passa-baixa. O resultado é limitado ao intervalo [0, 1].

    Parâmetros
    ----------
    frequencias_hz : np.ndarray | float
        Frequência ou conjunto de frequências, em Hz.

    Retorna
    -------
    np.ndarray
        Ganho linear em cada frequência.
    """
    frequencias = np.asarray(frequencias_hz, dtype=float)

    # log10(0) não é definido. Esta proteção também evita problemas numéricos.
    frequencias = np.maximum(frequencias, 1e-12)

    if MODO_GANHO == "bode_db":
        reta_1_db = BODE_RETA_1_A * np.log10(frequencias) + BODE_RETA_1_B
        reta_2_db = BODE_RETA_2_A * np.log10(frequencias) + BODE_RETA_2_B

        ganho_db = np.minimum(reta_1_db, reta_2_db)
        ganho_linear = 10 ** (ganho_db / 20)

    else:
        reta_1 = LINEAR_RETA_1_A * frequencias + LINEAR_RETA_1_B
        reta_2 = LINEAR_RETA_2_A * frequencias + LINEAR_RETA_2_B

        ganho_linear = np.minimum(reta_1, reta_2)

    return np.clip(ganho_linear, 0.0, 1.0)


def fase_rc_ideal(
    frequencias_hz: np.ndarray,
    frequencia_corte_hz: float | None,
) -> np.ndarray:
    """
    Calcula a fase aproximada de um filtro RC passa-baixa ideal.

    A fase só é aplicada se APLICAR_FASE_RC_IDEAL = True. Caso contrário,
    retorna fase zero para todos os harmônicos.

    Para um RC passa-baixa medido sobre o capacitor:

        H(f) = 1 / (1 + j f/fc)

    Logo:

        phi(f) = -arctan(f/fc)

    Parâmetros
    ----------
    frequencias_hz : np.ndarray
        Frequências dos harmônicos, em Hz.
    frequencia_corte_hz : float | None
        Frequência de corte, em Hz.

    Retorna
    -------
    np.ndarray
        Fase de cada harmônico, em radianos.
    """
    if not APLICAR_FASE_RC_IDEAL:
        return np.zeros_like(frequencias_hz, dtype=float)

    if frequencia_corte_hz is None:
        return np.zeros_like(frequencias_hz, dtype=float)

    return -np.arctan(frequencias_hz / frequencia_corte_hz)


def serie_fourier_onda_quadrada_filtrada(
    tempo_s: np.ndarray,
    frequencia_fundamental_hz: float,
    n_harmonicos: int,
) -> np.ndarray:
    """
    Reconstrói a onda quadrada após a filtragem passa-baixa.

    Cada harmônico da onda quadrada é multiplicado pelo ganho do filtro
    na frequência física correspondente:

        f_k = (2k - 1) f0

    A reconstrução fica:

        v_out(t) = sum A_k * G(f_k) * sin(2*pi*f_k*t + phi_k)

    Parâmetros
    ----------
    tempo_s : np.ndarray
        Malha temporal, em segundos.
    frequencia_fundamental_hz : float
        Frequência fundamental da onda quadrada, em Hz.
    n_harmonicos : int
        Número de harmônicos ímpares incluídos.

    Retorna
    -------
    np.ndarray
        Onda reconstruída após o filtro.
    """
    indices = indices_harmonicos_impares(n_harmonicos)
    frequencias = frequencias_harmonicos(frequencia_fundamental_hz, n_harmonicos)
    ganhos = ganho_passa_baixa(frequencias)

    frequencia_corte = frequencia_de_intersecao_das_retas()
    fases = fase_rc_ideal(frequencias, frequencia_corte)

    soma_filtrada = np.zeros_like(tempo_s)

    for indice, frequencia_hz, ganho, fase in zip(indices, frequencias, ganhos, fases):
        argumento = 2 * np.pi * frequencia_hz * tempo_s + fase
        soma_filtrada += ganho * np.sin(argumento) / indice

    return (4 / np.pi) * soma_filtrada


# =============================================================================
# 6. CLASSE PRINCIPAL DA APLICAÇÃO INTERATIVA
# =============================================================================

class AplicacaoFourierFiltroRC:
    """
    Aplicação interativa para visualizar Fourier + filtro passa-baixa.

    A janela possui três regiões:

    1. Domínio temporal:
        onda quadrada ideal, soma de Fourier antes do filtro e soma filtrada.

    2. Ganho em frequência:
        curva G(f) e pontos correspondentes aos harmônicos usados.

    3. Espectro de amplitudes:
        amplitudes dos harmônicos antes e depois da multiplicação por G(f_k).
    """

    def __init__(self) -> None:
        validar_configuracao()

        self.frequencia_fundamental_hz = FREQUENCIA_FUNDAMENTAL_HZ
        self.n_harmonicos = N_INICIAL
        self.mostrar_harmonicos = MOSTRAR_HARMONICOS_INICIALMENTE

        self.periodo_s = 1 / self.frequencia_fundamental_hz
        self.tempo_s = self._criar_malha_temporal()
        self.tempo_ms = 1000 * self.tempo_s

        self.frequencia_corte_hz = frequencia_de_intersecao_das_retas()
        self.frequencias_plot_hz = self._criar_malha_frequencias()

        self.fig, (self.ax_tempo, self.ax_ganho, self.ax_espectro) = plt.subplots(
            3,
            1,
            figsize=(11, 9),
            gridspec_kw={"height_ratios": [2.2, 1.2, 1.2]},
        )

        plt.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.17, hspace=0.45)

        self._criar_curvas_temporais()
        self._criar_curvas_ganho()
        self._criar_curvas_espectro()

        self._configurar_eixo_temporal()
        self._configurar_eixo_ganho()
        self._configurar_eixo_espectro()

        self._criar_slider()
        self._criar_checkbox()

        self.slider.on_changed(self._atualizar)
        self.check.on_clicked(self._alternar_harmonicos)

        self._atualizar(None)

    # -------------------------------------------------------------------------
    def _criar_malha_temporal(self) -> np.ndarray:
        """
        Cria a malha temporal usada no gráfico superior.

        A janela temporal é centrada em t = 0 e contém o número de períodos
        definido em NUM_PERIODOS_VISIVEIS.
        """
        t_min = -0.5 * NUM_PERIODOS_VISIVEIS * self.periodo_s
        t_max = +0.5 * NUM_PERIODOS_VISIVEIS * self.periodo_s
        return np.linspace(t_min, t_max, NUM_POINTS)

    # -------------------------------------------------------------------------
    def _criar_malha_frequencias(self) -> np.ndarray:
        """
        Cria a malha de frequências usada para desenhar a curva de ganho.

        A malha cobre desde abaixo da frequência fundamental até acima do
        maior harmônico permitido pelo slider.
        """
        maior_harmonico_hz = (2 * N_MAX - 1) * self.frequencia_fundamental_hz

        candidatos_min = [self.frequencia_fundamental_hz]
        candidatos_max = [maior_harmonico_hz]

        if self.frequencia_corte_hz is not None:
            candidatos_min.append(self.frequencia_corte_hz)
            candidatos_max.append(self.frequencia_corte_hz)

        f_min = max(1e-3, min(candidatos_min) / 10)
        f_max = max(candidatos_max) * 10

        return np.logspace(np.log10(f_min), np.log10(f_max), 1200)

    # -------------------------------------------------------------------------
    def _criar_curvas_temporais(self) -> None:
        """Cria as linhas do gráfico temporal."""
        y_referencia = onda_quadrada_referencia(
            self.tempo_s,
            self.frequencia_fundamental_hz,
        )

        y_fourier = serie_fourier_onda_quadrada(
            self.tempo_s,
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        y_filtrada = serie_fourier_onda_quadrada_filtrada(
            self.tempo_s,
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        (self.linha_referencia,) = self.ax_tempo.plot(
            self.tempo_ms,
            y_referencia,
            color=COR_REFERENCIA,
            linewidth=2,
            label="Onda quadrada ideal",
        )

        (self.linha_fourier,) = self.ax_tempo.plot(
            self.tempo_ms,
            y_fourier,
            color=COR_FOURIER,
            linewidth=2,
            label=f"Fourier antes do filtro (N = {self.n_harmonicos})",
        )

        (self.linha_filtrada,) = self.ax_tempo.plot(
            self.tempo_ms,
            y_filtrada,
            color=COR_FILTRADA,
            linewidth=2,
            label="Fourier após filtro",
        )

        self.linhas_harmonicos = []

        for _ in range(N_MAX):
            (linha,) = self.ax_tempo.plot(
                [],
                [],
                color=COR_HARMONICOS,
                linewidth=LARGURA_HARMONICOS,
                alpha=ALPHA_HARMONICOS,
                visible=False,
            )
            self.linhas_harmonicos.append(linha)

        (self.linha_legenda_harmonicos,) = self.ax_tempo.plot(
            [],
            [],
            color=COR_HARMONICOS,
            linewidth=LARGURA_HARMONICOS,
            alpha=ALPHA_HARMONICOS,
            label="Harmônicos individuais",
        )

    # -------------------------------------------------------------------------
    def _criar_curvas_ganho(self) -> None:
        """Cria a curva de ganho e os pontos dos harmônicos."""
        ganho_curva = ganho_passa_baixa(self.frequencias_plot_hz)

        (self.linha_ganho,) = self.ax_ganho.plot(
            self.frequencias_plot_hz,
            ganho_curva,
            color=COR_GANHO,
            linewidth=2,
            label="Ganho passa-baixa G(f)",
        )

        (self.pontos_ganho_harmonicos,) = self.ax_ganho.plot(
            [],
            [],
            "o",
            color=COR_FOURIER,
            markersize=4,
            label="G(fk) nos harmônicos usados",
        )

        if self.frequencia_corte_hz is not None:
            self.ax_ganho.axvline(
                self.frequencia_corte_hz,
                color="black",
                linestyle="--",
                linewidth=1,
                alpha=0.7,
                label=f"Interseção ≈ {self.frequencia_corte_hz:.1f} Hz",
            )

    # -------------------------------------------------------------------------
    def _criar_curvas_espectro(self) -> None:
        """Cria os pontos do espectro antes e depois do filtro."""
        (self.pontos_amplitudes_entrada,) = self.ax_espectro.plot(
            [],
            [],
            "o",
            color=COR_FOURIER,
            markersize=4,
            label="Amplitude Fourier antes do filtro",
        )

        (self.pontos_amplitudes_filtradas,) = self.ax_espectro.plot(
            [],
            [],
            "o",
            color=COR_FILTRADA,
            markersize=4,
            label="Amplitude após multiplicar por G(fk)",
        )

    # -------------------------------------------------------------------------
    def _configurar_eixo_temporal(self) -> None:
        """Configura título, eixos e legenda do gráfico temporal."""
        titulo = (
            f"Onda quadrada e filtragem passa-baixa — "
            f"f0 = {self.frequencia_fundamental_hz:.1f} Hz, "
            f"N = {self.n_harmonicos}"
        )

        self.ax_tempo.set_title(titulo, fontsize=14)
        self.ax_tempo.set_xlabel("Tempo (ms)")
        self.ax_tempo.set_ylabel("Amplitude normalizada")
        self.ax_tempo.set_ylim(Y_MIN, Y_MAX)
        self.ax_tempo.grid(True, linestyle="--", alpha=0.5)
        self.ax_tempo.legend(loc="upper right")

    # -------------------------------------------------------------------------
    def _configurar_eixo_ganho(self) -> None:
        """Configura o gráfico de ganho em frequência."""
        self.ax_ganho.set_xscale("log")
        self.ax_ganho.set_ylabel("Ganho linear")
        self.ax_ganho.set_ylim(-0.05, 1.10)
        self.ax_ganho.grid(True, which="both", linestyle="--", alpha=0.5)
        self.ax_ganho.legend(loc="upper right")

    # -------------------------------------------------------------------------
    def _configurar_eixo_espectro(self) -> None:
        """Configura o gráfico das amplitudes harmônicas."""
        self.ax_espectro.set_xscale("log")
        self.ax_espectro.set_xlabel("Frequência (Hz)")
        self.ax_espectro.set_ylabel("Amplitude")
        self.ax_espectro.set_ylim(-0.05, 1.35)
        self.ax_espectro.grid(True, which="both", linestyle="--", alpha=0.5)
        self.ax_espectro.legend(loc="upper right")

    # -------------------------------------------------------------------------
    def _criar_slider(self) -> None:
        """Adiciona o slider para controlar o número de harmônicos."""
        ax_slider = plt.axes([0.18, 0.07, 0.70, 0.03])

        self.slider = Slider(
            ax=ax_slider,
            label="N harmônicos ímpares",
            valmin=N_MIN,
            valmax=N_MAX,
            valinit=N_INICIAL,
            valstep=1,
        )

    # -------------------------------------------------------------------------
    def _criar_checkbox(self) -> None:
        """Adiciona checkbox para mostrar ou ocultar harmônicos individuais."""
        ax_check = plt.axes([0.02, 0.045, 0.13, 0.07])

        self.check = CheckButtons(
            ax=ax_check,
            labels=["Harmônicos"],
            actives=[self.mostrar_harmonicos],
        )

    # -------------------------------------------------------------------------
    def _alternar_harmonicos(self, _label: str) -> None:
        """Alterna a visibilidade dos harmônicos individuais."""
        self.mostrar_harmonicos = not self.mostrar_harmonicos
        self._atualizar(None)

    # -------------------------------------------------------------------------
    def _atualizar(self, _valor) -> None:
        """
        Atualiza todos os gráficos quando o slider ou a checkbox é alterado.
        """
        self.n_harmonicos = validar_n_harmonicos(self.slider.val)

        self._atualizar_grafico_temporal()
        self._atualizar_grafico_ganho()
        self._atualizar_grafico_espectro()

        self.fig.canvas.draw_idle()

    # -------------------------------------------------------------------------
    def _atualizar_grafico_temporal(self) -> None:
        """Atualiza a onda de Fourier antes e depois do filtro."""
        y_fourier = serie_fourier_onda_quadrada(
            self.tempo_s,
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        y_filtrada = serie_fourier_onda_quadrada_filtrada(
            self.tempo_s,
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        self.linha_fourier.set_ydata(y_fourier)
        self.linha_filtrada.set_ydata(y_filtrada)

        self.linha_fourier.set_label(
            f"Fourier antes do filtro (N = {self.n_harmonicos})"
        )

        titulo = (
            f"Onda quadrada e filtragem passa-baixa — "
            f"f0 = {self.frequencia_fundamental_hz:.1f} Hz, "
            f"N = {self.n_harmonicos}"
        )

        self.ax_tempo.set_title(titulo, fontsize=14)

        self._atualizar_harmonicos_individuais()

        self.ax_tempo.legend(loc="upper right")

    # -------------------------------------------------------------------------
    def _atualizar_harmonicos_individuais(self) -> None:
        """
        Atualiza os harmônicos individuais no domínio temporal.

        Eles são mostrados apenas quando a checkbox está ativa, pois muitos
        harmônicos simultâneos podem poluir o gráfico.
        """
        harmonicos = harmonicos_individuais(
            self.tempo_s,
            self.frequencia_fundamental_hz,
            N_MAX,
        )

        for i, linha in enumerate(self.linhas_harmonicos):
            linha.set_data(self.tempo_ms, harmonicos[i])

            visivel = self.mostrar_harmonicos and (i < self.n_harmonicos)
            linha.set_visible(visivel)

        self.linha_legenda_harmonicos.set_visible(self.mostrar_harmonicos)

    # -------------------------------------------------------------------------
    def _atualizar_grafico_ganho(self) -> None:
        """Atualiza os pontos G(fk) dos harmônicos usados."""
        frequencias = frequencias_harmonicos(
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        ganhos = ganho_passa_baixa(frequencias)

        self.pontos_ganho_harmonicos.set_data(frequencias, ganhos)

    # -------------------------------------------------------------------------
    def _atualizar_grafico_espectro(self) -> None:
        """Atualiza as amplitudes antes e depois da multiplicação pelo ganho."""
        frequencias = frequencias_harmonicos(
            self.frequencia_fundamental_hz,
            self.n_harmonicos,
        )

        amplitudes_entrada = amplitudes_fourier_onda_quadrada(
            self.n_harmonicos,
        )

        ganhos = ganho_passa_baixa(frequencias)
        amplitudes_filtradas = amplitudes_entrada * ganhos

        self.pontos_amplitudes_entrada.set_data(
            frequencias,
            amplitudes_entrada,
        )

        self.pontos_amplitudes_filtradas.set_data(
            frequencias,
            amplitudes_filtradas,
        )


# =============================================================================
# 7. FUNÇÃO PRINCIPAL
# =============================================================================

def main() -> None:
    """
    Executa a aplicação interativa.
    """
    app = AplicacaoFourierFiltroRC()
    plt.show()


# =============================================================================
# 8. PONTO DE ENTRADA DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()