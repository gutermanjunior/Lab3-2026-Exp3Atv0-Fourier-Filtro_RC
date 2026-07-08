# =============================================================================
# Arquivo: fourier_square_wave_interactive.py
# Título: Visualização Interativa da Série de Fourier de uma Onda Quadrada
#
# Descrição:
#     Este programa mostra como uma onda quadrada pode ser aproximada pela soma
#     parcial dos seus harmônicos ímpares na série de Fourier.
#
# Objetivo didático:
#     Ilustrar a construção progressiva da onda quadrada, o papel dos harmônicos
#     ímpares e o aparecimento do fenómeno de Gibbs.
#
# Autor: Guterman Junior
# Data: 20260707
# Versão: 1.0
#
# Dependências:
#     numpy
#     matplotlib
#
# Execução:
#     python fourier_square_wave_interactive.py
#
# Modelo matemático:
#     f_N(x) = (4/pi) * sum_{k=1}^{N} sin((2k - 1)x)/(2k - 1)
#
# Limitações:
#     A onda quadrada ideal é descontínua. Nos pontos de salto, a série de
#     Fourier converge para o valor médio dos limites laterais.
#
# Nota:
#     Código escrito para fins educacionais, priorizando clareza e legibilidade.
# =============================================================================

# =============================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

# =============================================================================
# 2. CONSTANTES E PARÂMETROS GLOBAIS
# =============================================================================
# Número de pontos no domínio – uma malha densa para capturar as oscilações
# do fenómeno de Gibbs perto das descontinuidades.
NUM_POINTS = 2000

# Domínio horizontal: dois períodos completos
X_MIN, X_MAX = -2 * np.pi, 2 * np.pi

# Parâmetros do slider
N_MIN = 1
N_MAX = 50
N_INICIAL = 3

# Limite vertical para visualizar o overshoot de Gibbs (~ 1,18)
Y_MIN, Y_MAX = -1.5, 1.5

# Cores e estilos
COR_REFERENCIA = "black"
COR_SOMA = "red"
ALPHA_HARMONICOS = 0.4
LARGURA_HARMONICOS = 0.7

# =============================================================================
# 3. FUNÇÕES MATEMÁTICAS
# =============================================================================
def validar_n_harmonicos(n: int) -> int:
    """
    Valida e ajusta o número de harmónicos ímpares usados na soma.

    Parâmetros
    ----------
    n : int
        Valor escolhido pelo utilizador (pode vir do slider).

    Retorna
    -------
    int
        Valor inteiro >= 1.
    """
    return max(1, int(n))


def onda_quadrada_referencia(x: np.ndarray) -> np.ndarray:
    """
    Onda quadrada ideal de referência.

    Como a série de Fourier é ímpar e converge para o valor médio nos
    pontos de descontinuidade, usamos `sign(sin(x))` que vale
      +1 em (0, π), (2π, 3π), …
      -1 em (−π, 0), (π, 2π), …
       0 nos múltiplos de π (média dos limites laterais).

    Parâmetros
    ----------
    x : np.ndarray
        Malha de abcissas.

    Retorna
    -------
    np.ndarray
        Valores da onda quadrada ideal.
    """
    return np.sign(np.sin(x))


def serie_fourier_onda_quadrada(x: np.ndarray, n_harmonicos: int) -> np.ndarray:
    """
    Soma parcial da série de Fourier da onda quadrada ímpar.

    f_N(x) = (4/π) Σ_{k=1}^{N} sin((2k−1)x) / (2k−1)

    Parâmetros
    ----------
    x : np.ndarray
        Malha de abcissas.
    n_harmonicos : int
        Número de harmónicos ímpares incluídos (k = 1 … N).

    Retorna
    -------
    np.ndarray
        Aproximação de Fourier de ordem N.
    """
    soma = np.zeros_like(x)
    for k in range(1, n_harmonicos + 1):
        soma += np.sin((2 * k - 1) * x) / (2 * k - 1)
    return (4 / np.pi) * soma


def harmonicos_individuais(x: np.ndarray, n_harmonicos: int) -> list:
    """
    Calcula cada harmónico ímpar que compõe a soma parcial.

    Parâmetros
    ----------
    x : np.ndarray
        Malha de abcissas.
    n_harmonicos : int
        Número de harmónicos a calcular.

    Retorna
    -------
    list[np.ndarray]
        Lista com a contribuição de cada k, na ordem k = 1, 2, …, N.
    """
    harmonicos = []
    for k in range(1, n_harmonicos + 1):
        y = (4 / np.pi) * np.sin((2 * k - 1) * x) / (2 * k - 1)
        harmonicos.append(y)
    return harmonicos


# =============================================================================
# 4. CLASSE PRINCIPAL DA APLICAÇÃO INTERATIVA
# =============================================================================
class AplicacaoFourier:
    """
    Aplicação interativa que ilustra a aproximação de uma onda quadrada
    pela sua série de Fourier.

    Atributos
    ---------
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes.Axes
    x : np.ndarray
    n_harmonicos : int
    mostrar_harmonicos : bool
    linha_referencia : matplotlib.lines.Line2D
    linha_soma : matplotlib.lines.Line2D
    linhas_harmonicos : list[matplotlib.lines.Line2D]
    legenda_harmonicos : matplotlib.lines.Line2D
    slider : matplotlib.widgets.Slider
    check : matplotlib.widgets.CheckButtons
    """

    def __init__(self):
        # Malha de abcissas comum a todos os gráficos
        self.x = np.linspace(X_MIN, X_MAX, NUM_POINTS)

        # Estado inicial
        self.n_harmonicos = N_INICIAL
        self.mostrar_harmonicos = True

        # Criação da figura e eixos
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.10, bottom=0.25)  # espaço para slider e check

        # Desenhar as curvas iniciais
        self._criar_curvas()

        # Configurar eixos (título, legenda, grelha, limites)
        self._configurar_eixos()

        # Adicionar controlos interativos
        self._criar_slider()
        self._criar_checkbox()

        # Ligar os callbacks
        self.slider.on_changed(self._atualizar)
        self.check.on_clicked(self._alternar_harmonicos)

    # -------------------------------------------------------------------------
    def _criar_curvas(self) -> None:
        """Desenha (ou cria placeholders para) todas as curvas."""
        # Onda quadrada de referência
        y_ref = onda_quadrada_referencia(self.x)
        (self.linha_referencia,) = self.ax.plot(
            self.x, y_ref,
            color=COR_REFERENCIA, linewidth=2, label="Onda quadrada ideal"
        )

        # Soma parcial de Fourier
        y_soma = serie_fourier_onda_quadrada(self.x, self.n_harmonicos)
        (self.linha_soma,) = self.ax.plot(
            self.x, y_soma,
            color=COR_SOMA, linewidth=2, label="Soma parcial (N = {})".format(self.n_harmonicos)
        )

        # Harmónicos individuais (criamos uma linha para cada possível harmónico)
        self.linhas_harmonicos = []
        # Usamos um mapa de cores qualitativo para distinguir os harmónicos
        cores = plt.cm.tab10(np.linspace(0, 1, N_MAX))
        for k in range(1, N_MAX + 1):
            (linha,) = self.ax.plot(
                [], [],  # dados vazios, serão preenchidos em _atualizar()
                color=cores[k - 1],
                linewidth=LARGURA_HARMONICOS,
                alpha=ALPHA_HARMONICOS,
                visible=(k <= self.n_harmonicos and self.mostrar_harmonicos),
            )
            self.linhas_harmonicos.append(linha)

        # Linha fictícia para a legenda dos harmónicos
        (self.legenda_harmonicos,) = self.ax.plot(
            [], [],
            color="gray", linewidth=LARGURA_HARMONICOS, alpha=ALPHA_HARMONICOS,
            label="Harmónicos"
        )
        # Visibilidade inicial coerente
        self.legenda_harmonicos.set_visible(self.mostrar_harmonicos)

        # Preencher os harmónicos visíveis inicialmente
        self._atualizar_harmonicos()

    # -------------------------------------------------------------------------
    def _configurar_eixos(self) -> None:
        """Aplica títulos, rótulos, grelha e limites ao eixo principal."""
        self.ax.set_title(
            f"Aproximação da Onda Quadrada — N = {self.n_harmonicos}",
            fontsize=14
        )
        self.ax.set_xlabel("x", fontsize=12)
        self.ax.set_ylabel("f(x)", fontsize=12)
        self.ax.set_xlim(X_MIN, X_MAX)
        self.ax.set_ylim(Y_MIN, Y_MAX)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.legend(loc="upper right")

    # -------------------------------------------------------------------------
    def _criar_slider(self) -> None:
        """Adiciona o slider para controlar o número de harmónicos N."""
        ax_slider = plt.axes([0.15, 0.10, 0.70, 0.03])
        self.slider = Slider(
            ax_slider,
            "N (harmónicos)",
            valmin=N_MIN,
            valmax=N_MAX,
            valinit=N_INICIAL,
            valstep=1,      # apenas valores inteiros
        )

    # -------------------------------------------------------------------------
    def _criar_checkbox(self) -> None:
        """Adiciona a caixa de verificação para mostrar/ocultar harmónicos."""
        ax_check = plt.axes([0.02, 0.02, 0.25, 0.08])
        self.check = CheckButtons(
            ax_check,
            ["Mostrar harmónicos"],
            [self.mostrar_harmonicos],
        )

    # -------------------------------------------------------------------------
    def _alternar_harmonicos(self, label: str) -> None:
        """
        Callback da caixa de verificação.
        Alterna a visibilidade de todos os harmónicos.
        """
        self.mostrar_harmonicos = not self.mostrar_harmonicos
        self._atualizar(None)  # redesenha tudo

    # -------------------------------------------------------------------------
    def _atualizar(self, val) -> None:
        """
        Callback chamado quando o slider é movido ou a checkbox é alterada.
        Recalcula a soma parcial e os harmónicos visíveis, e atualiza o gráfico.
        """
        # Obter o novo N do slider
        self.n_harmonicos = validar_n_harmonicos(self.slider.val)

        # Atualizar a soma parcial
        y_soma = serie_fourier_onda_quadrada(self.x, self.n_harmonicos)
        self.linha_soma.set_ydata(y_soma)

        # Atualizar o título
        self.ax.set_title(
            f"Aproximação da Onda Quadrada — N = {self.n_harmonicos}",
            fontsize=14
        )

        # Atualizar a legenda da soma parcial
        self.linha_soma.set_label(f"Soma parcial (N = {self.n_harmonicos})")

        # Atualizar os harmónicos individuais
        self._atualizar_harmonicos()

        # Forçar redesenho
        self.fig.canvas.draw_idle()

    # -------------------------------------------------------------------------
    def _atualizar_harmonicos(self) -> None:
        """
        Recalcula os dados de cada harmónico e ajusta a visibilidade
        de acordo com N e com a checkbox.
        """
        # Calcular os primeiros N_MAX harmónicos (apenas os necessários)
        todos_harmonicos = harmonicos_individuais(self.x, N_MAX)

        for k in range(1, N_MAX + 1):
            linha = self.linhas_harmonicos[k - 1]
            y_k = todos_harmonicos[k - 1]
            linha.set_data(self.x, y_k)

            # Visível apenas se k <= N e a checkbox estiver ativa
            visivel = (k <= self.n_harmonicos) and self.mostrar_harmonicos
            linha.set_visible(visivel)

        # A linha da legenda segue a checkbox
        self.legenda_harmonicos.set_visible(self.mostrar_harmonicos)

        # Reconstruir a legenda para refletir a nova label da soma
        self.ax.legend(loc="upper right")


# =============================================================================
# 5. FUNÇÃO PRINCIPAL
# =============================================================================
def main() -> None:
    """
    Ponto de entrada do programa.
    Cria a aplicação interativa e mostra a janela.
    """
    app = AplicacaoFourier()
    plt.show()


# =============================================================================
# 6. PONTO DE ENTRADA DO PROGRAMA
# =============================================================================
if __name__ == "__main__":
    main()