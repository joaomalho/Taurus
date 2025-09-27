import math
from backend.funcionalities.formulas import Formulas


class RiskManagerTechnical ():

    def __init__(self):
        self

    def relevance_candle(self):
        '''
        Determine whether the targets have already been reached following pattern detection, if not, consider them as active targets.
        Additionally, evaluate which pattern should be prioritized if multiple patterns are detected.
        '''

    def stoploss_manager():
        pass

    def take_profit_manager():
        pass

    def signal_decision_rsi(self, rsi_now, upper_level, lower_level):

        if rsi_now >= upper_level:
            rsi_signal = 'Sell'
        elif rsi_now <= lower_level:
            rsi_signal = 'Buy'
        else:
            rsi_signal = 'Flat'
        return rsi_signal

    def signal_decision_bbands(self, last_close, lower_band, upper_band):

        if last_close <= lower_band:
            bbands_signal = 'Buy'
        elif last_close >= upper_band:
            bbands_signal = 'Sell'
        else:
            bbands_signal = 'Flat'
        return bbands_signal

    def signal_decision_adx(self, adx_now):

        if adx_now < 20:
            adx_signal = 'Weak Trend'
        elif 20 <= adx_now < 50:
            adx_signal = 'Strong Trend'
        elif 50 <= adx_now < 75:
            adx_signal = 'Very Strong Trend'
        else:
            adx_signal = 'Extremely Strong Trend'
        return adx_signal

    def signal_decision_crossover(self, ema_low, ema_mid, ema_high):

        if ema_low > ema_mid > ema_high:
            crossover_signal = 'Buy'
        elif ema_low < ema_mid < ema_high:
            crossover_signal = 'Sell'
        else:
            crossover_signal = 'Flat'
        return crossover_signal

    def stoploss_candles_conditions(self, signal, stoploss, future_close_prices):
        """
        Verify if stoploss were hitted in candle patterns
        """
        if stoploss is None:
            return "N/A"

        if signal == -100:
            return "Hit Stoploss (Above)" if any(close > stoploss for close in future_close_prices) else "No Hit"

        if signal == 100:
            return "Hit Stoploss (Below)" if any(close < stoploss for close in future_close_prices) else "No Hit"

        return "N/A"


class RiskManagerFundamental():

    def __init__(self):
        self.stoploss = None
        self.takeprofit = None

    COLORS = {
        "verygood": "#1cf467",
        "good":     "#0f8a3b",
        "neutral":  "#6b7280",
        "bad":      "#9b3232",
        "verybad":  "#ff1414",
        "nodata":   "#9E9E9E",
    }

    METRIC_RULES = {
        "NetDebtEbitda": [
            (0,          "Very Strong", "verygood"),
            (1,          "Strong",      "good"),
            (3,          "Neutral",     "neutral"),
            (math.inf,   "Weak",        "bad"),
        ],
        "InterestCoverageEbit": [
            (3,          "Weak",        "bad"),
            (8,          "Neutral",     "neutral"),
            (math.inf,   "Strong",      "good"),
        ],
        "CurrentRatio": [
            (1.0,        "Not Good (In Debt)",                  "bad"),
            (1.5,        "Tight Margin to Debt",                "neutral"),
            (2.0,        "Good Debt Coverage",                  "good"),
            (math.inf,   "Perfect Coverage (Double +)",         "verygood"),
        ],
        "QuickRatio": [
            (0.8,        "Not Good (In Debt)",                  "bad"),
            (1.0,        "Tight Margin to Debt",                "neutral"),
            (1.5,        "Good Debt Coverage",                  "good"),
            (math.inf,   "Perfect Coverage (Double +)",         "verygood"),
        ],
        "EnterpriseFCFYield": [
            (2.5,        "Expensive",                           "bad"),
            (4.0,        "Fair",                                "neutral"),
            (math.inf,   "Cheap",                               "verygood"),
        ],
        "EquityFCFYield": [
            (3.0,        "Expensive",                           "bad"),
            (5.0,        "Fair",                                "neutral"),
            (math.inf,   "Cheap",                               "verygood"),
        ],
        "PriceToSale": [
            (2.0,        "Cheap",                               "verygood"),
            (6.0,        "Fair",                                "neutral"),
            (math.inf,   "Expensive",                           "bad"),
        ],
        "evEbitda": [
            (8.0,        "Cheap",                               "verygood"),
            (12.0,       "Fair",                                "neutral"),
            (math.inf,   "Expensive",                           "bad"),
        ],
    }

    METRIC_MESSAGES_PT = {
        "NetDebtEbitda": {
            "verygood": lambda v: {
                "short":  f"**Net Debt / EBITDA =** {v:.2f}",
                "detail": (
                        "**Significado:**\n"
                        "- A empresa apresenta caixa líquido (tem mais dinheiro em caixa do que dívida).\n\n"
                        "**Interpretação:**\n"
                        "- A a empresa encontra-se em posição de caixa líquido, conseguindo teoricamente liquidar toda a dívida de imediato. Situação de grande solidez financeira.\n"
                        "- Não depende de financiamento externo para sustentar operações e pode até reforçar dividendos ou investir sem necessidade de se endividar.\n\n"
                        "**Risco:**\n"
                        "- Muito baixo — o balanço funciona como um verdadeiro “colchão” contra crises."
                ),
                "tooltip": "≤0: caixa líquido (muito sólido)."
            },
            "good": lambda v: {
                "short":  f"**Net Debt / EBITDA =** {v:.2f}",
                "detail": (
                        "**Significado:**\n"
                        "- A dívida líquida é inferior a um ano de geração de EBITDA.\n\n"
                        "**Interpretação:**\n"
                        "- A empresa tem baixa alavancagem e consegue reduzir dívida rapidamente sem comprometer operações.\n"
                        "- Precisaria de apenas um ano de geração operacional para liquidar a sua dívida líquida. Perfil de risco bastante saudável.\n\n"
                        "**Risco:**\n"
                        "- Conservador — ainda robusta perante cenários adversos."
                    ),
                "tooltip": "≤1: baixo endividamento."
            },
            "neutral": lambda v: {
                "short":  f"**Net Debt / EBITDA =** {v:.2f}",
                "detail": (
                        "**Significado:**\n"
                        "- A dívida líquida corresponde a 1 a 3 anos de EBITDA.\n\n"
                        "**Interpretação:**\n"
                        "- É um nível comum em setores mais intensivos em capital; aceitável, mas requer monitorização.\n"
                        "- A empresa apresenta alavancagem moderada. É aceitável, mas aumenta a sensibilidade a ciclos económicos ou choques de mercado.\n\n"
                        "**Risco:**\n"
                        "- Moderado — uma quebra nos lucros ou subida dos juros pode exercer pressão."
                    ),
                "tooltip": "1–3: alavancagem moderada."
            },
            "bad": lambda v: {
                "short":  f"**Net Debt / EBITDA =** {v:.2f}",
                "detail": (
                        "**Significado:**\n"
                        "- A dívida líquida supera 3 anos de geração de EBITDA.\n\n"
                        "**Interpretação: **\n"
                        "- A empresa está altamente alavancada, mais dependente de condições de crédito favoráveis e de resultados estáveis.\n"
                        "- Encontra-se bastante endividada e dependente da estabilidade operacional e das condições de financiamento.\n"
                        "- Pequenas quedas no EBITDA podem comprometer a capacidade de honrar compromissos.\n\n"
                        "**Risco: **\n"
                        "- Elevado — maior vulnerabilidade a recessões, subida de juros ou quebras de EBITDA."
                ),
                "tooltip": ">3: endividamento elevado."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Net Debt / EBITDA.**",
                "detail": "Informação insuficiente para avaliar o nível de alavancagem.",
                "tooltip": "Sem dados."
            },
        },
        "InterestCoverageEbit": {
            "good": lambda v: {
                "short":  f"**Interest Coverage (EBIT) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- Quantas vezes o EBIT cobre os encargos de juros.\n\n"
                    "**Interpretação:**\n"
                    "- Cobertura elevada dos juros, com margem para absorver quedas de resultados ou subidas de taxas.\n"
                    "- Menor dependência de refinanciamentos em condições adversas.\n\n"
                    "**Risco:**\n"
                    "- Baixo — elevada capacidade de serviço da dívida."
                ),
                "tooltip": ">8×: cobertura forte (saudável). 3–8×: adequada. ≤3×: fraca."
            },
            "neutral": lambda v: {
                "short":  f"**Interest Coverage (EBIT) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- EBIT cobre os juros num intervalo moderado.\n\n"
                    "**Interpretação:**\n"
                    "- Situação aceitável, mas sensível a descidas do EBIT ou a subidas de juros.\n"
                    "- Requer acompanhamento regular do custo da dívida e da rentabilidade.\n\n"
                    "**Risco:**\n"
                    "- Moderado — pode degradar em ciclos menos favoráveis."
                ),
                "tooltip": "3–8×: cobertura adequada (neutro). >8×: forte. ≤3×: fraca."
            },
            "bad": lambda v: {
                "short":  f"**Interest Coverage (EBIT) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- Cobertura dos juros baixa (EBIT cobre pouco os encargos financeiros).\n\n"
                    "**Interpretação:**\n"
                    "- Maior probabilidade de pressão de liquidez se o EBIT cair.\n"
                    "- Pode necessitar de refinanciamento, alongamento de prazos ou redução de dívida.\n\n"
                    "**Risco:**\n"
                    "- Elevado — vulnerável a choques operacionais ou financeiros."
                ),
                "tooltip": "≤3×: cobertura fraca (risco elevado). 3–8×: adequada. >8×: forte."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Interest Coverage (EBIT).**",
                "detail": "Informação insuficiente para avaliar a cobertura de juros (EBIT/juros).",
                "tooltip": "Sem dados."
            },
        },
        "CurrentRatio": {
            "verygood": lambda v: {
                "short":  f"**Current Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Relação entre ativos correntes e passivos correntes (liquidez de curto prazo).\n\n"
                    "**Interpretação:**\n"
                    "- Cobertura folgada das obrigações de curto prazo; almofada de liquidez confortável.\n"
                    "- Pode indicar gestão conservadora de fundo de maneio.\n\n"
                    "**Risco:**\n"
                    "- Baixo — boa capacidade de cumprir compromissos imediatos."
                ),
                "tooltip": "≥2.0: muito bom (folgado). 1.5–2.0: saudável. 1.0–1.5: apertado. ≤1.0: fraco."
            },
            "good": lambda v: {
                "short":  f"**Current Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Ativos correntes cobrem confortavelmente os passivos correntes.\n\n"
                    "**Interpretação:**\n"
                    "- Liquidez saudável com alguma folga.\n"
                    "- Boa disciplina de capital circulante.\n\n"
                    "**Risco:**\n"
                    "- Moderado-baixo — perfil equilibrado de liquidez."
                ),
                "tooltip": "1.5–2.0: saudável. ≥2.0: muito bom. 1.0–1.5: apertado. ≤1.0: fraco."
            },
            "neutral": lambda v: {
                "short":  f"**Current Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Cobertura próxima do limiar mínimo (entre 1.0 e 1.5).\n\n"
                    "**Interpretação:**\n"
                    "- Situação aceitável mas apertada; dependente da conversão de inventários/recebimentos em caixa.\n"
                    "- Convém monitorizar prazos de recebimento e rotação de inventários.\n\n"
                    "**Risco:**\n"
                    "- Moderado — sensível a atrasos de clientes ou choques de curto prazo."
                ),
                "tooltip": "1.0–1.5: apertado (neutro). 1.5–2.0: saudável. ≥2.0: muito bom. ≤1.0: fraco."
            },
            "bad": lambda v: {
                "short":  f"**Current Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Ativos correntes não cobrem os passivos correntes (≤1.0).\n\n"
                    "**Interpretação:**\n"
                    "- Risco de pressão de liquidez no curto prazo; pode exigir reforço de caixa ou renegociação de prazos.\n"
                    "- Maior dependência de linhas de crédito.\n\n"
                    "**Risco:**\n"
                    "- Elevado — probabilidade acrescida de tensão de caixa."
                ),
                "tooltip": "≤1.0: fraco (risco de liquidez). 1.0–1.5: apertado. 1.5–2.0: saudável. ≥2.0: muito bom."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Current Ratio.**",
                "detail": "Informação insuficiente para avaliar a liquidez de curto prazo.",
                "tooltip": "Sem dados."
            },
        },
        "QuickRatio": {
            "verygood": lambda v: {
                "short":  f"**Quick Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Liquidez imediata (exclui inventários) face a dívidas de curto prazo.\n\n"
                    "**Interpretação:**\n"
                    "- Cobertura forte das obrigações imediatas com ativos líquidos (caixa + recebimentos).\n"
                    "- Menor dependência de vender inventário para cumprir prazos.\n\n"
                    "**Risco:**\n"
                    "- Baixo — robustez de liquidez no curtíssimo prazo."
                ),
                "tooltip": "≥1.5: forte (muito bom). 1.0–1.5: bom. 0.8–1.0: apertado. <0.8: fraco."
            },
            "good": lambda v: {
                "short":  f"**Quick Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Ativos líquidos cobrem de forma adequada as obrigações de curto prazo.\n\n"
                    "**Interpretação:**\n"
                    "- Liquidez imediata suficiente, desde que a cobrança ocorra em prazos normais.\n"
                    "- Perfil equilibrado sem excesso de caixa.\n\n"
                    "**Risco:**\n"
                    "- Moderado-baixo — condição estável."
                ),
                "tooltip": "1.0–1.5: bom. ≥1.5: muito bom. 0.8–1.0: apertado. <0.8: fraco."
            },
            "neutral": lambda v: {
                "short":  f"**Quick Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Cobertura apertada com ativos rapidamente realizáveis.\n\n"
                    "**Interpretação:**\n"
                    "- Dependente de cobrança atempada de clientes; pequena derrapagem pode gerar tensão.\n"
                    "- Convém reforçar caixa ou melhorar prazos de recebimento.\n\n"
                    "**Risco:**\n"
                    "- Moderado — pouca folga de segurança."
                ),
                "tooltip": "0.8–1.0: apertado (neutro). 1.0–1.5: bom. ≥1.5: muito bom. <0.8: fraco."
            },
            "bad": lambda v: {
                "short":  f"**Quick Ratio =** {v:.2f}",
                "detail": (
                    "**Significado:**\n"
                    "- Ativos líquidos insuficientes para cobrir dívidas imediatas (<0.8).\n\n"
                    "**Interpretação:**\n"
                    "- Elevada probabilidade de tensão de caixa sem financiamento externo ou melhoria rápida da rotação.\n"
                    "- Pode exigir medidas de gestão de capital circulante.\n\n"
                    "**Risco:**\n"
                    "- Elevado — vulnerabilidade no curtíssimo prazo."
                ),
                "tooltip": "<0.8: fraco (risco imediato). 0.8–1.0: apertado. 1.0–1.5: bom. ≥1.5: muito bom."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Quick Ratio.**",
                "detail": "Informação insuficiente para avaliar a liquidez imediata.",
                "tooltip": "Sem dados."
            },
        },
        "trailingPE": {
            "verygood": lambda ctx: {
                # ctx traz trailing, forward, sector, score
                "short":  f"**Trailing P/E =** {ctx['trailing']:.2f}× — **Undervalued** face ao setor/forward.",
                "detail": (
                    "**Significado:**\n"
                    "- A ação negocia com desconto vs. o setor e/ou o P/E desce no *forward*, refletindo expectativa de crescimento.\n\n"
                    "**Interpretação:**\n"
                    f"- **Sector P/E:** {ctx['sector']:.2f}× | **Forward P/E:** {ctx['forward']:.2f}×.\n"
                    "- A relação de P/E sugere avaliação atrativa, assumindo que as estimativas se confirmam.\n"
                    "- Usa o gráfico de *earnings* (estimado/real/surprise) para validar consistência.\n\n"
                    "**Risco:**\n"
                    "- Moderado/baixo — risco principal é a execução (lucros têm de aparecer)."
                ),
                "tooltip": "Trailing < Sector, Forward < Sector e/ou Trailing > Forward (crescimento à frente)."
            },
            "good": lambda ctx: {
                "short":  f"**Trailing P/E =** {ctx['trailing']:.2f}× — **Undervalued** moderado.",
                "detail": (
                    "**Significado:**\n"
                    "- Desconto moderado face ao setor e/ou melhoria no *forward*.\n\n"
                    "**Interpretação:**\n"
                    f"- **Sector P/E:** {ctx['sector']:.2f}× | **Forward P/E:** {ctx['forward']:.2f}×.\n"
                    "- Sinal positivo, mas dependente de estimativas e *mix* de margens.\n\n"
                    "**Risco:**\n"
                    "- Moderado — monitorizar *earnings surprise* e revisões de consenso."
                ),
                "tooltip": "Algumas condições favoráveis vs setor/forward; desconto não extremo."
            },
            "neutral": lambda ctx: {
                "short":  f"**Trailing P/E =** {ctx['trailing']:.2f}× — **Neutral Valued**.",
                "detail": (
                    "**Significado:**\n"
                    "- Múltiplo em linha com o setor e/ou sem melhoria material no *forward*.\n\n"
                    "**Interpretação:**\n"
                    f"- **Sector P/E:** {ctx['sector']:.2f}× | **Forward P/E:** {ctx['forward']:.2f}×.\n"
                    "- Avaliação equilibrada; performance vai depender do *delivery* operacional.\n\n"
                    "**Risco:**\n"
                    "- Médio — sem margem de segurança evidente, mas também sem prémio excessivo."
                ),
                "tooltip": "Em linha com o setor; sem grande desconto/prémio."
            },
            "bad": lambda ctx: {
                "short":  f"**Trailing P/E =** {ctx['trailing']:.2f}× — **Overvalued**.",
                "detail": (
                    "**Significado:**\n"
                    "- Prémio vs. setor e/ou *forward* não mostra alívio suficiente.\n\n"
                    "**Interpretação:**\n"
                    f"- **Sector P/E:** {ctx['sector']:.2f}× | **Forward P/E:** {ctx['forward']:.2f}×.\n"
                    "- Mercado embute expectativas otimistas; sensível a surpresas negativas.\n\n"
                    "**Risco:**\n"
                    "- Elevado — compressão de múltiplos se o crescimento desiludir."
                ),
                "tooltip": "Trailing ≥ Sector e/ou Forward não compensa o prémio."
            },
            "verybad": lambda ctx: {
                "short":  f"**Trailing P/E =** {ctx['trailing']:.2f}× — **Very High Overvalued**.",
                "detail": (
                    "**Significado:**\n"
                    "- Avaliação exigente face ao setor, pouco suporte no *forward*.\n\n"
                    "**Interpretação:**\n"
                    f"- **Sector P/E:** {ctx['sector']:.2f}× | **Forward P/E:** {ctx['forward']:.2f}×.\n"
                    "- Elevada dependência de crescimento acelerado e de *execution flawless*.\n\n"
                    "**Risco:**\n"
                    "- Alto — forte vulnerabilidade a *misses* de resultados."
                ),
                "tooltip": "Prémio acentuado vs setor; forward não justifica."
            },
            "nodata": lambda ctx: {
                "short":  "**Sem dados suficientes para P/E.**",
                "detail": "Faltam valores de trailing/forward/sector para avaliar.",
                "tooltip": "Sem dados."
            }
        },
        "EquityFCFYield": {
            "verygood": lambda v: {
                "short":  f"**Equity FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Cheap*: o fluxo de caixa livre gerado é elevado face ao valor do capital próprio.\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação atrativa; maior capacidade para dividendos, *buybacks*, desalavancagem ou investimento sem diluição.\n"
                    "- Pode indicar *margin of safety*, assumindo que o FCF é recorrente e sustentável.\n\n"
                    "**Risco:**\n"
                    "- Baixo/moderado — ainda assim, verificar qualidade do FCF (one-offs, capitalização de custos, ciclo de CAPEX)."
                ),
                "tooltip": ">5%: barato (muito bom). 3–5%: razoável. ≤3%: caro."
            },
            "neutral": lambda v: {
                "short":  f"**Equity FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Fair*: o FCF face ao valor do capital próprio está em linha com o razoável.\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação equilibrada; retorno em caixa adequado para o risco médio do setor.\n"
                    "- Monitorizar ciclo de investimento/FCF e necessidades de CAPEX de manutenção.\n\n"
                    "**Risco:**\n"
                    "- Moderado — sensível a volatilidade do FCF e a revisões de expectativas."
                ),
                "tooltip": "3–5%: razoável (neutro). >5%: barato. ≤3%: caro."
            },
            "bad": lambda v: {
                "short":  f"**Equity FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Expensive*: baixo retorno de caixa livre face ao valor do capital próprio.\n\n"
                    "**Interpretação:**\n"
                    "- Mercado embute expectativas de crescimento/melhoria operacional; pouco retorno imediato em caixa.\n"
                    "- Menor folga para remunerar acionistas sem recorrer a dívida ou diluição.\n\n"
                    "**Risco:**\n"
                    "- Elevado — se o crescimento desiludir, a compressão de múltiplos pode penalizar a ação."
                ),
                "tooltip": "≤3%: caro (fraco). 3–5%: razoável. >5%: barato."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Equity FCF Yield.**",
                "detail": "Informação insuficiente para avaliar o retorno de caixa livre para os acionistas.",
                "tooltip": "Sem dados."
            },
        },
        "EnterpriseFCFYield": {
            "verygood": lambda v: {
                "short":  f"**Enterprise FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Cheap*: a empresa gera fluxo de caixa livre elevado face ao seu valor empresarial (dívida + capital próprio − caixa).\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação atrativa baseada em caixa; maior capacidade para desalavancar, investir e remunerar acionistas sem pressão de financiamento.\n"
                    "- Pode indicar *margin of safety*, assumindo FCF recorrente e sustentável.\n\n"
                    "**Risco:**\n"
                    "- Baixo/moderado — validar qualidade do FCF (one-offs, sazonalidade, CAPEX de manutenção)."
                ),
                "tooltip": ">4: barato (muito bom). 2,5–4: razoável. ≤2,5: caro."
            },
            "neutral": lambda v: {
                "short":  f"**Enterprise FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Fair*: retorno de caixa livre em linha com um nível razoável para o risco do negócio.\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação equilibrada; retorno adequado, sem grande almofada.\n"
                    "- Monitorizar ciclo de investimento e estabilidade do FCF.\n\n"
                    "**Risco:**\n"
                    "- Moderado — sensível a volatilidade do FCF e a revisões de expectativas."
                ),
                "tooltip": "2,5–4: razoável (neutro). >4: barato. ≤2,5: caro."
            },
            "bad": lambda v: {
                "short":  f"**Enterprise FCF Yield =** {v*100:.2f}%",
                "detail": (
                    "**Significado:**\n"
                    "- *Expensive*: baixo FCF face ao valor empresarial.\n\n"
                    "**Interpretação:**\n"
                    "- Mercado precifica crescimento/melhoria operacional; pouco retorno imediato em caixa.\n"
                    "- Menor folga para desalavancar ou remunerar acionistas sem recorrer a dívida/diluição.\n\n"
                    "**Risco:**\n"
                    "- Elevado — vulnerável a desilusões no crescimento e compressão de múltiplos."
                ),
                "tooltip": "≤2,5: caro (fraco). 2,5–4: razoável. >4: barato."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para Enterprise FCF Yield.**",
                "detail": "Informação insuficiente para avaliar o retorno de caixa livre face ao valor empresarial.",
                "tooltip": "Sem dados."
            },
        },
        "PriceToSale": {
            "verygood": lambda v: {
                "short":  f"**Price to Sales (P/S) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Cheap*: preço baixo face às vendas anuais.\n\n"
                    "**Interpretação:**\n"
                    "- Pode ser atrativo, sobretudo se a empresa tiver margens em expansão e boa rotação.\n"
                    "- Confirmar qualidade das receitas (mix, recorrência) e rentabilidade.\n\n"
                    "**Risco:**\n"
                    "- Baixo/moderado — atenção a negócios de baixa margem onde P/S pode enganar."
                ),
                "tooltip": "≤2×: barato (muito bom). 2–6×: razoável. >6×: caro."
            },
            "neutral": lambda v: {
                "short":  f"**Price to Sales (P/S) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Fair*: preço em linha com as vendas para o perfil do setor.\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação equilibrada; justifica-se se margens/ crescimento forem médios.\n"
                    "- Acompanhar evolução de margem bruta/operacional.\n\n"
                    "**Risco:**\n"
                    "- Moderado — dependente da conversão de vendas em lucro/FCF."
                ),
                "tooltip": "2–6×: razoável (neutro). ≤2×: barato. >6×: caro."
            },
            "bad": lambda v: {
                "short":  f"**Price to Sales (P/S) =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Expensive*: preço alto face às vendas.\n\n"
                    "**Interpretação:**\n"
                    "- Só se justifica com **crescimento acelerado** e/ou **margens muito altas**.\n"
                    "- Se o *mix* de receitas mudar ou o crescimento abrandar, o múltiplo pode comprimir.\n\n"
                    "**Risco:**\n"
                    "- Elevado — vulnerável a desilusões no crescimento e na rentabilidade."
                ),
                "tooltip": ">6×: caro (fraco). 2–6×: razoável. ≤2×: barato."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para P/S.**",
                "detail": "Informação insuficiente para avaliar o preço face às vendas.",
                "tooltip": "Sem dados."
            },
        },
        "evEbitda": {
            "verygood": lambda v: {
                "short":  f"**EV / EBITDA =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Cheap*: valor empresarial baixo face à geração operacional (EBITDA).\n\n"
                    "**Interpretação:**\n"
                    "- Atraente se o EBITDA for sustentável e não houver risco de CAPEX/ dívida oculto.\n"
                    "- Útil para comparar empresas com estruturas de capital distintas.\n\n"
                    "**Risco:**\n"
                    "- Baixo/moderado — confirmar qualidade do EBITDA (ajustes, sazonalidade, *one-offs*)."
                ),
                "tooltip": "≤8×: barato (muito bom). 8–12×: razoável. >12×: caro."
            },
            "neutral": lambda v: {
                "short":  f"**EV / EBITDA =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Fair*: relação equilibrada entre valor empresarial e EBITDA.\n\n"
                    "**Interpretação:**\n"
                    "- Avaliação em linha com pares/sector.\n"
                    "- Evolução vai depender de crescimento e disciplina de investimento.\n\n"
                    "**Risco:**\n"
                    "- Moderado — sem grande almofada, mas também sem prémio excessivo."
                ),
                "tooltip": "8–12×: razoável (neutro). ≤8×: barato. >12×: caro."
            },
            "bad": lambda v: {
                "short":  f"**EV / EBITDA =** {v:.2f}×",
                "detail": (
                    "**Significado:**\n"
                    "- *Expensive*: valor empresarial elevado face à geração operacional.\n\n"
                    "**Interpretação:**\n"
                    "- Mercado embute expectativas de crescimento/margens mais fortes.\n"
                    "- Sensível a *misses* de resultados ou subida de custos/juros.\n\n"
                    "**Risco:**\n"
                    "- Elevado — potencial de compressão do múltiplo se as expectativas falharem."
                ),
                "tooltip": ">12×: caro (fraco). 8–12×: razoável. ≤8×: barato."
            },
            "nodata": lambda v: {
                "short": "**Sem dados para EV / EBITDA.**",
                "detail": "Informação insuficiente para avaliar o valor empresarial face ao EBITDA.",
                "tooltip": "Sem dados."
            },
        },
    }

    PE_TEXT_TO_BUCKET = {
        "Very Low Undervalued": "verygood",
        "Low Undervalued":      "verygood",
        "Undervalued":          "good",
        "Neutral Valued":       "neutral",
        "Overvalued":           "bad",
        "High Overvalued":      "bad",
        "Very High Overvalued": "verybad",
    }

    # ---------- Funções utilitárias ----------
    @staticmethod
    def _is_number(x):
        return isinstance(x, (int, float)) and not math.isnan(x)

    def classify_value(self, key: str, value):
        """Aplica as regras do registry para obter (evaluation, bucket)."""
        if value is None or not self._is_number(value):
            return "No Data", "nodata"
        rules = self.METRIC_RULES.get(key)
        if not rules:
            # fallback se não houver regra registada
            return "Indefinido", "neutral"
        for ub, label, bucket in rules:
            if value <= ub:
                return label, bucket
        return "Indefinido", "neutral"

    def messages_for(self, key: str, value, bucket: str, lang: str = "en"):
        """Gera mensagens a partir dos templates do registry."""
        reg = self.METRIC_MESSAGES_PT if lang == "en" else self.METRIC_MESSAGES_PT
        maker = (reg.get(key, {}).get(bucket) or reg.get(key, {}).get("nodata"))
        return maker(value) if callable(maker) else {"short": "", "detail": "", "tooltip": ""}

    # ---------- Emissão compatível com o front ----------
    def _set_eval(self, out: dict, key: str, text: str):
        out[f"{key}_evaluation"] = text
        bucket = out.get(f"{key}_bucket") or {
            "Very Strong": "verygood", "Strong": "good", "Neutral": "neutral", "Weak": "bad", "No Data": "nodata"
        }.get(text, "neutral")
        out[f"{key}_bucket"] = bucket
        out[f"{key}_color"] = self.COLORS.get(bucket, "#6b7280")

    def _set_message(self, out: dict, key: str, which: str, text: str):
        k = f"{key}_messages"
        if k not in out or not isinstance(out[k], dict):
            out[k] = {}
        out[k][which] = text

    def _emit_full(self, out: dict, key: str, value, evaluation: str, bucket: str, msgs: dict):
        out[key] = value if value is not None else None
        out[f"{key}_bucket"] = bucket         
        self._set_eval(out, key, evaluation)
        for k, v in (msgs or {}).items():
            self._set_message(out, key, k, v)

    def classify_trailing_pe(self, trailing, sector, forward):
        """
        Replica o teu score (3 condições) e devolve (evaluation_text, bucket, score).
        """
        if None in (trailing, sector, forward) or \
                not all(self._is_number(x) for x in (trailing, sector, forward)):
            return "No Data", "nodata", None

        score = 0
        score += 1 if trailing < sector else -1 if trailing > sector else 0
        score += 1 if forward < sector else -1 if forward > sector else 0
        score += 1 if trailing > forward else -1 if trailing < forward else 0

        text = {
            3:  "Very Low Undervalued",
            2:  "Low Undervalued",
            1:  "Undervalued",
            0:  "Neutral Valued",
            -1: "Overvalued",
            -2: "High Overvalued",
        }.get(score, "Very High Overvalued")

        bucket = self.PE_TEXT_TO_BUCKET.get(text, "neutral")
        return text, bucket, score

    def evaluate_metrics(self, metrics):
        """
        Evaluate fundamental metrics.
        """

        fm = Formulas()

        evaluated_metrics = {}

        # ----- Imports ----- #
        kpis = metrics.get('kpis', {})

        # ----- VALUATIONS ----- #
        # ----- PEs ----- #
        trailing_pe = fm.safe_round(kpis.get("trailingPE"))
        sector_pe = fm.safe_round(kpis.get("sectorTrailingPE"))
        forward_pe = fm.safe_round(kpis.get("forwardPE"))

        # valores crus (continua a expor no payload normal)
        evaluated_metrics["trailingPE"] = trailing_pe if trailing_pe is not None else None
        evaluated_metrics["sectorTrailingPE"] = sector_pe if sector_pe is not None else None
        evaluated_metrics["forwardPE"] = forward_pe if forward_pe is not None else None

        # classificar + mensagens (dedicado ao P/E)
        eval_pe, bucket_pe, score_pe = self.classify_trailing_pe(trailing_pe, sector_pe, forward_pe)

        # mensagens com contexto (passa dicionário em vez de número)
        ctx = {"trailing": trailing_pe or float("nan"),
               "forward": forward_pe or float("nan"),
               "sector": sector_pe or float("nan"),
               "score": score_pe}

        msgs_pe = (self.METRIC_MESSAGES_PT.get("trailingPE", {}).get(bucket_pe, self.METRIC_MESSAGES_PT.get("trailingPE", {}).get("nodata")))

        msgs_pe = msgs_pe(ctx) if callable(msgs_pe) else {"short": "", "detail": "", "tooltip": ""}

        self._emit_full(evaluated_metrics, "trailingPE", trailing_pe, eval_pe, bucket_pe, msgs_pe)

        # ----- EV / EBITDA
        ev_ebitda = fm.safe_round(kpis.get("evEbitda"))
        eval_ev_ebitda, bucket_ev_ebitda = self.classify_value("evEbitda", ev_ebitda)
        msgs_ev_ebitda = self.messages_for("evEbitda", ev_ebitda, bucket_ev_ebitda, lang="en")
        self._emit_full(evaluated_metrics, "evEbitda", ev_ebitda, eval_ev_ebitda, bucket_ev_ebitda, msgs_ev_ebitda)

        # ----- Prise To Sale
        ps = fm.safe_round(kpis.get("PriceToSale"))
        eval_ps, bucket_ps = self.classify_value("PriceToSale", ps)
        msgs_ps = self.messages_for("PriceToSale", ps, bucket_ps, lang="en")
        self._emit_full(evaluated_metrics, "PriceToSale", ps, eval_ps, bucket_ps, msgs_ps)

        # ----- Equity FCF Yield
        eqfy = kpis.get("EquityFCFYield")
        eval_eqfy, bucket_eqfy = self.classify_value("EquityFCFYield", eqfy)
        msgs_eqfy = self.messages_for("EquityFCFYield", eqfy, bucket_eqfy, lang="en")
        self._emit_full(evaluated_metrics, "EquityFCFYield", eqfy, eval_eqfy, bucket_eqfy, msgs_eqfy)

        # ----- Enterprise FCF Yield
        efy = kpis.get("EnterpriseFCFYield")
        eval_efy, bucket_efy = self.classify_value("EnterpriseFCFYield", efy)
        msgs_efy = self.messages_for("EnterpriseFCFYield", efy, bucket_efy, lang="en")
        self._emit_full(evaluated_metrics, "EnterpriseFCFYield", efy, eval_efy, bucket_efy, msgs_efy)

        # ----- Finantial Health ----- #
        # --- Net Debt / EBITDA ---
        nd = fm.safe_round(kpis.get("NetDebtEbitda"))
        eval_nd, bucket_nd = self.classify_value("NetDebtEbitda", nd)
        msgs_nd = self.messages_for("NetDebtEbitda", nd, bucket_nd, lang="en")
        self._emit_full(evaluated_metrics, "NetDebtEbitda", nd, eval_nd, bucket_nd, msgs_nd)

        # --- Interest Coverage (EBIT) ---
        ic = fm.safe_round(kpis.get("InterestCoverageEbit"))
        eval_ic, bucket_ic = self.classify_value("InterestCoverageEbit", ic)
        msgs_ic = self.messages_for("InterestCoverageEbit", ic, bucket_ic, lang="en")
        self._emit_full(evaluated_metrics, "InterestCoverageEbit", ic, eval_ic, bucket_ic, msgs_ic)

        # --- Current Ratio ---
        cr = fm.safe_round(kpis.get("CurrentRatio"))
        eval_cr, bucket_cr = self.classify_value("CurrentRatio", cr)
        msgs_cr = self.messages_for("CurrentRatio", cr, bucket_cr, lang="en")
        self._emit_full(evaluated_metrics, "CurrentRatio", cr, eval_cr, bucket_cr, msgs_cr)

        # --- Quick Ratio ---
        qr = fm.safe_round(kpis.get("QuickRatio"))
        eval_qr, bucket_qr = self.classify_value("QuickRatio", qr)
        msgs_qr = self.messages_for("QuickRatio", qr, bucket_qr, lang="en")
        self._emit_full(evaluated_metrics, "QuickRatio", qr, eval_qr, bucket_qr, msgs_qr)

        # ----- Profitability ----- #
        # ----- Operational Margin
        operating_margin = fm.safe_round(kpis.get("OperationalMargin"))
        evaluated_metrics["OperationalMargin"] = operating_margin if operating_margin is not None else None

        if operating_margin is None:
            text_OperationalMargin = "No Data"
        else:
            if operating_margin <= 10:
                text_OperationalMargin = "Not Good - High Operational Costs or Difficulties to Get Revenue"
            elif operating_margin <= 20:
                text_OperationalMargin = "Healthy - Healthy Operational Management"
            else:
                text_OperationalMargin = "Good - Efficient Costs Management"

        self._set_eval(evaluated_metrics, "OperationalMargin", text_OperationalMargin)

        # ----- FCF Margin
        fcf_margin = fm.safe_round(kpis.get("FcfMargin"))
        evaluated_metrics["FcfMargin"] = fcf_margin if fcf_margin is not None else None

        if fcf_margin is None:
            text_FcfMargin = "No Data"
        else:
            if fcf_margin <= 10:
                text_FcfMargin = "Not Good - High Operational Costs or Difficulties to Get Revenue"
            elif fcf_margin <= 20:
                text_FcfMargin = "Healthy - Healthy Operational Management"
            else:
                text_FcfMargin = "Good - Efficient Costs Management"

        self._set_eval(evaluated_metrics, "FcfMargin", text_FcfMargin)

        # ----- ROE
        roe = fm.safe_round(kpis.get("ROE"))
        evaluated_metrics["ROE"] = roe if roe is not None else None

        if roe is None:
            text_ROE = "No Data"
        else:
            if roe <= 8:
                text_ROE = "Weak"
            elif roe <= 15:
                text_ROE = "Healthy"
            else:
                text_ROE = "Strong"

        self._set_eval(evaluated_metrics, "ROE", text_ROE)

        # ----- ROA
        roa = fm.safe_round(kpis.get("ROA"))
        evaluated_metrics["ROA"] = roa if roa is not None else None

        if roa is None:
            text_ROA = "No Data"
        else:
            if roa <= 3:
                text_ROA = "Weak"
            elif roa <= 7:
                text_ROA = "Healthy"
            else:
                text_ROA = "Strong"

        self._set_eval(evaluated_metrics, "ROA", text_ROA)

        # ----- Capital Efficiency ----- #
        # ----- ROIC
        roic = fm.safe_round(kpis.get("ROIC"))
        evaluated_metrics["ROIC"] = roic if roic is not None else None

        if roic is None:
            text_ROIC = "No Data"
        else:
            if roic <= 6:
                text_ROIC = "Weak"
            elif roic <= 12:
                text_ROIC = "Healthy"
            else:
                text_ROIC = "Strong"

        self._set_eval(evaluated_metrics, "ROIC", text_ROIC)

        # ----- EVA
        eva = fm.safe_round(kpis.get("EVA"))
        evaluated_metrics["EVA"] = eva if eva is not None else None

        if eva is None:
            text_EVA = "No Data"
        else:
            if eva <= 0:
                text_EVA = "Destroys Value"
            elif eva <= 12:
                text_EVA = "Cover Capital Expenses"
            else:
                text_EVA = "Generate Value"

        self._set_eval(evaluated_metrics, "EVA", text_EVA)

        # ----- Growth ----- #
        # ----- GrowthReveneuYoY
        growth_reveneu_yoy = fm.safe_round(kpis.get("GrowthReveneuYoY"))
        evaluated_metrics["GrowthReveneuYoY"] = growth_reveneu_yoy if growth_reveneu_yoy is not None else None

        if growth_reveneu_yoy is None:
            text_GrowthReveneuYoY = "No Data"
        else:
            if growth_reveneu_yoy <= 4:
                text_GrowthReveneuYoY = "Weak"
            elif growth_reveneu_yoy <= 10:
                text_GrowthReveneuYoY = "Healthy"
            else:
                text_GrowthReveneuYoY = "Strong"

        self._set_eval(evaluated_metrics, "GrowthReveneuYoY", text_GrowthReveneuYoY)

        # ----- CagrGrowthReveneuYoY
        cagr_growth_reveneu_yoy = fm.safe_round(kpis.get("CagrGrowthReveneuYoY"))
        evaluated_metrics["CagrGrowthReveneuYoY"] = cagr_growth_reveneu_yoy if cagr_growth_reveneu_yoy is not None else None

        if cagr_growth_reveneu_yoy is None:
            text_CagrGrowthReveneuYoY = "No Data"
        else:
            if cagr_growth_reveneu_yoy <= 4:
                text_CagrGrowthReveneuYoY = "Weak"
            elif cagr_growth_reveneu_yoy <= 10:
                text_CagrGrowthReveneuYoY = "Healthy"
            else:
                text_CagrGrowthReveneuYoY = "Strong"

        self._set_eval(evaluated_metrics, "CagrGrowthReveneuYoY", text_CagrGrowthReveneuYoY)

        # ----- GrowthEPSYoY
        growth_eps_yoy = fm.safe_round(kpis.get("GrowthEPSYoY"))
        evaluated_metrics["GrowthEPSYoY"] = growth_eps_yoy if growth_eps_yoy is not None else None

        if growth_eps_yoy is None:
            text_GrowthEPSYoY = "No Data"
        else:
            if growth_eps_yoy <= 4:
                text_GrowthEPSYoY = "Weak"
            elif growth_eps_yoy <= 10:
                text_GrowthEPSYoY = "Healthy"
            else:
                text_GrowthEPSYoY = "Strong"

        self._set_eval(evaluated_metrics, "GrowthEPSYoY", text_GrowthEPSYoY)

        # ----- CagrGrowthEPSYoY
        cagr_growth_eps_yoy = fm.safe_round(kpis.get("CagrGrowthEPSYoY"))
        evaluated_metrics["CagrGrowthEPSYoY"] = cagr_growth_eps_yoy if cagr_growth_eps_yoy is not None else None

        if cagr_growth_eps_yoy is None:
            text_CagrGrowthEPSYoY = "No Data"
        else:
            if cagr_growth_eps_yoy <= 4:
                text_CagrGrowthEPSYoY = "Weak"
            elif cagr_growth_eps_yoy <= 10:
                text_CagrGrowthEPSYoY = "Healthy"
            else:
                text_CagrGrowthEPSYoY = "Strong"

        self._set_eval(evaluated_metrics, "CagrGrowthEPSYoY", text_CagrGrowthEPSYoY)

        # ----- Dividend ----- #
        # ----- Dividend Coverage Ratio
        div_coverage_raw = fm.safe_round(kpis.get("divCoverageRate"))
        evaluated_metrics["divCoverageRate"] = div_coverage_raw if div_coverage_raw is not None else None

        if div_coverage_raw is None:
            text_divCoverageRate = "No Data"
        else:
            if div_coverage_raw <= 1:
                text_divCoverageRate = "No Coverage"
            elif div_coverage_raw <= 1.5:
                text_divCoverageRate = "Bad Coverage (Cut)"
            elif div_coverage_raw <= 3:
                text_divCoverageRate = "Good Coverage"
            else:
                text_divCoverageRate = "Very Good Coverage (Greedy)"

        self._set_eval(evaluated_metrics, "divCoverageRate", text_divCoverageRate)

        # ----- payout_ratio
        payout_ratio = fm.safe_round(kpis.get("PayoutRatio"))
        evaluated_metrics["PayoutRatio"] = payout_ratio if payout_ratio is not None else None

        if payout_ratio is None:
            text_PayoutRatio = "No Data"
        else:
            if payout_ratio <= 0.3:
                text_PayoutRatio = "Very Good Coverage (Greedy)"
            elif payout_ratio <= 0.6:
                text_PayoutRatio = "Good Coverage"
            elif payout_ratio <= 0.7:
                text_PayoutRatio = "Bad Coverage (Cut)"
            else:
                text_PayoutRatio = "No Coverage"

        self._set_eval(evaluated_metrics, "PayoutRatio", text_PayoutRatio)

        # ----- CagrGrowthDividend3y
        cagr_growth_dividend3y = fm.safe_round(kpis.get("CagrGrowthDividend3y"))
        evaluated_metrics["CagrGrowthDividend3y"] = cagr_growth_dividend3y if cagr_growth_dividend3y is not None else None

        if cagr_growth_dividend3y is None:
            text_CagrGrowthDividend3y = "No Data"
        else:
            if cagr_growth_dividend3y <= 0.00:
                text_CagrGrowthDividend3y = "Cut on Dividends"
            elif cagr_growth_dividend3y <= 0.05:
                text_CagrGrowthDividend3y = "Moderated"
            else:
                text_CagrGrowthDividend3y = "Good Growth"

        self._set_eval(evaluated_metrics, "CagrGrowthDividend3y", text_CagrGrowthDividend3y)

        # ----- CagrGrowthDividend5y
        cagr_growth_dividend5y = fm.safe_round(kpis.get("CagrGrowthDividend5y"))
        evaluated_metrics["CagrGrowthDividend5y"] = cagr_growth_dividend5y if cagr_growth_dividend5y is not None else None

        if cagr_growth_dividend5y is None:
            text_CagrGrowthDividend5y = "No Data"
        else:
            if cagr_growth_dividend5y <= 0.00:
                text_CagrGrowthDividend5y = "Cut on Dividends"
            elif cagr_growth_dividend5y <= 0.05:
                text_CagrGrowthDividend5y = "Moderated"
            else:
                text_CagrGrowthDividend5y = "Good Growth"

        self._set_eval(evaluated_metrics, "CagrGrowthDividend5y", text_CagrGrowthDividend5y)

        # ----- ShareHolderYield
        shareholder_yield = fm.safe_round(kpis.get("ShareHolderYield"))
        evaluated_metrics["ShareHolderYield"] = shareholder_yield if shareholder_yield is not None else None

        if shareholder_yield is None:
            text_ShareHolderYield = "No Data"
        else:
            if shareholder_yield <= 0.02:
                text_ShareHolderYield = "Low"
            elif shareholder_yield <= 0.05:
                text_ShareHolderYield = "Moderated"
            else:
                text_ShareHolderYield = "Excellent"

        self._set_eval(evaluated_metrics, "ShareHolderYield", text_ShareHolderYield)

        # ----- Extras ----- #
        # ----- Net Worth
        net_worth = fm.safe_round(metrics.get('finantial_health', {}).get("NetWorth"))
        evaluated_metrics["NetWorth"] = net_worth if net_worth is not None else None

        if net_worth is None:
            text_NetWorth = "No Data"
        else:
            text_NetWorth = "Good" if net_worth > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "NetWorth", text_NetWorth)

        # Short Term Debt Coverage
        short_debt_cov = fm.safe_round(metrics.get('finantial_health', {}).get("ShortTermDebtCoverage"))
        evaluated_metrics["ShortTermDebtCoverage"] = short_debt_cov if short_debt_cov is not None else None

        if short_debt_cov is None:
            text_ShortTermDebtCoverage = "No Data"
        else:
            text_ShortTermDebtCoverage = "Good" if short_debt_cov > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "ShortTermDebtCoverage", text_ShortTermDebtCoverage)

        # Long Term Debt Coverage
        long_debt_cov = fm.safe_round(metrics.get('finantial_health', {}).get("LongTermDebtCoverage"))
        evaluated_metrics["LongTermDebtCoverage"] = long_debt_cov if long_debt_cov is not None else None

        if long_debt_cov is None:
            text_LongTermDebtCoverage = "No Data"
        else:
            text_LongTermDebtCoverage = "Good" if long_debt_cov > 0 else "Not Good (In Debt)"

        self._set_eval(evaluated_metrics, "LongTermDebtCoverage", text_LongTermDebtCoverage)

        # Assets Growth
        total_assets_cagr = fm.safe_round(metrics.get('finantial_health', {}).get("TotalAssetsCAGR"))
        evaluated_metrics["TotalAssetsCAGR"] = total_assets_cagr if total_assets_cagr is not None else None

        if total_assets_cagr is None or math.isnan(total_assets_cagr):
            text_TotalAssetsCAGR = "No Data"
        else:
            text_TotalAssetsCAGR = "Good" if total_assets_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalAssetsCAGR", text_TotalAssetsCAGR)

        # Liabilities Growth
        total_liabilities_cagr = fm.safe_round(metrics.get('finantial_health', {}).get("TotalLiabilitiesCAGR"))
        evaluated_metrics["TotalLiabilitiesCAGR"] = total_liabilities_cagr if total_liabilities_cagr is not None else None

        if total_liabilities_cagr is None or math.isnan(total_liabilities_cagr):
            text_TotalLiabilitiesCAGR = "No Data"
        else:
            text_TotalLiabilitiesCAGR = "Good" if total_liabilities_cagr <= 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalLiabilitiesCAGR", text_TotalLiabilitiesCAGR)

        # Stockholders Equity
        stockholders_equity_cagr = fm.safe_round(metrics.get('finantial_health', {}).get("StockholdersEquityCAGR"))
        evaluated_metrics["StockholdersEquityCAGR"] = stockholders_equity_cagr if stockholders_equity_cagr is not None else None

        if stockholders_equity_cagr is None or math.isnan(stockholders_equity_cagr):
            text_StockholdersEquityCAGR = "No Data"
        else:
            text_StockholdersEquityCAGR = "Good" if stockholders_equity_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "StockholdersEquityCAGR", text_StockholdersEquityCAGR)

        # Profitability - Cost of Revenue CAGR
        cost_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("CostOfRevenueCAGR"))

        # Armazenar o valor bruto
        evaluated_metrics["CostOfRevenueCAGR"] = cost_revenue_cagr if cost_revenue_cagr is not None else None

        # Avaliação
        if cost_revenue_cagr is None or math.isnan(cost_revenue_cagr):
            text_CostOfRevenueCAGR = "No Data"
        else:
            if cost_revenue_cagr <= 0:
                text_CostOfRevenueCAGR = "Good"
            else:
                text_CostOfRevenueCAGR = "Not Good"

        self._set_eval(evaluated_metrics, "CostOfRevenueCAGR", text_CostOfRevenueCAGR)

        total_revenue_cagr = fm.safe_round(metrics.get('profitability', {}).get("TotalRevenueCAGR"))
        evaluated_metrics["TotalRevenueCAGR"] = total_revenue_cagr if total_revenue_cagr is not None else None

        if total_revenue_cagr is None or math.isnan(total_revenue_cagr):
            text_TotalRevenueCAGR = "No Data"
        else:
            text_TotalRevenueCAGR = "Good" if total_revenue_cagr > 0 else "Not Good"

        self._set_eval(evaluated_metrics, "TotalRevenueCAGR", text_TotalRevenueCAGR)

        # Cash
        # Free Cashflow Yield
        fcf_yield = fm.safe_round(metrics.get('cashflow', {}).get("FreeCashflowYield"))
        evaluated_metrics["FreeCashflowYield"] = fcf_yield if fcf_yield is not None else None

        if fcf_yield is None:
            text_FreeCashflowYield = "No Data"
        elif fcf_yield <= 2:
            text_FreeCashflowYield = "Overvalued / Bad to Generate Cash"
        elif fcf_yield <= 5:
            text_FreeCashflowYield = "Healthy / Consistent to Generates Cash"
        else:
            text_FreeCashflowYield = "Undervalued / Highly Profitable"

        self._set_eval(evaluated_metrics, "FreeCashflowYield", text_FreeCashflowYield)

        # Ratios

        # Cash Ratio
        cash_ratio = fm.safe_round(metrics.get('ratios', {}).get("CashRatio"))
        evaluated_metrics["CashRatio"] = cash_ratio if cash_ratio is not None else None

        if cash_ratio is None:
            text_CashRatio = "No Data"
        else:
            if cash_ratio <= 50:
                text_CashRatio = "Not Good (In Debt)"
            elif cash_ratio <= 100:
                text_CashRatio = "Good Debt Coverage"
            else:
                text_CashRatio = "Good Debt Coverage (Too Conservative)"

        self._set_eval(evaluated_metrics, "CashRatio", text_CashRatio)

        # Gross Margin
        gross_margin = fm.safe_round(metrics.get('ratios', {}).get("GrossMargin"))
        evaluated_metrics["GrossMargin"] = gross_margin if gross_margin is not None else None

        if gross_margin is None:
            text_GrossMargin = "No Data"
        else:
            if gross_margin <= 25:
                text_GrossMargin = "Not Good - Short Margins or High Costs"
            elif gross_margin <= 40:
                text_GrossMargin = "Healthy - Healthy Margins Good Management"
            else:
                text_GrossMargin = "Good - Efficient Costs Management"

        self._set_eval(evaluated_metrics, "GrossMargin", text_GrossMargin)

        # Gross Margin Growth
        gross_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("GrossMarginCAGR"))
        evaluated_metrics["GrossMarginCAGR"] = gross_margin_cagr if gross_margin_cagr is not None else None

        if gross_margin_cagr is None or math.isnan(gross_margin_cagr):
            text_GrossMarginCAGR = "No Data"
        else:
            text_GrossMarginCAGR = (
                "Good" if gross_margin_cagr > 0 else "Not Good"
            )

        self._set_eval(evaluated_metrics, "GrossMarginCAGR", text_GrossMarginCAGR)

        # Operational Margin Growth
        operating_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("OperatingMarginCAGR"))
        evaluated_metrics["OperatingMarginCAGR"] = operating_margin_cagr if operating_margin_cagr is not None else None

        if operating_margin_cagr is None or math.isnan(operating_margin_cagr):
            text_OperatingMarginCAGR = "No Data"
        else:
            if operating_margin_cagr <= 0:
                text_OperatingMarginCAGR = "Not Good"
            else:
                text_OperatingMarginCAGR = "Good"

        self._set_eval(evaluated_metrics, "OperatingMarginCAGR", text_OperatingMarginCAGR)

        # Profit Margin
        profit_margin = fm.safe_round(metrics.get('ratios', {}).get("ProfitMargin"))
        evaluated_metrics["ProfitMargin"] = profit_margin if profit_margin is not None else None

        if profit_margin is None:
            text_ProfitMargin = "No Data"
        else:
            if profit_margin <= 5:
                text_ProfitMargin = "Not Good - High Operational Costs or Operational Problems"
            elif profit_margin <= 10:
                text_ProfitMargin = "Moderated - Potential but Need Improvements"
            elif profit_margin <= 20:
                text_ProfitMargin = "Healthy - Healthy and Solid Management"
            else:
                text_ProfitMargin = "Good - Highly Profitable and Eficient Profit Generate"

        self._set_eval(evaluated_metrics, "ProfitMargin", text_ProfitMargin)

        # Profit Margin Growth
        profit_margin_cagr = fm.safe_round(metrics.get('ratios', {}).get("ProfitMarginCAGR"))
        evaluated_metrics["ProfitMarginCAGR"] = profit_margin_cagr if profit_margin_cagr is not None else None

        if profit_margin_cagr is None or math.isnan(profit_margin_cagr):
            text_ProfitMarginCAGR = "No Data"
        else:
            if profit_margin_cagr <= 0:
                text_ProfitMarginCAGR = "Not Good - Declining or No Growth"
            else:
                text_ProfitMarginCAGR = "Good - Growing Profitability Over Time"

        self._set_eval(evaluated_metrics, "ProfitMarginCAGR", text_ProfitMarginCAGR)

        # Return On Equity
        return_on_equity = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquity"))
        evaluated_metrics["ReturnOnEquity"] = return_on_equity if return_on_equity is not None else None

        if return_on_equity is None:
            text_ReturnOnEquity = "No Data"
        else:
            if return_on_equity <= 10:
                text_ReturnOnEquity = "Not Good - Low Efficiency on Equity Use"
            elif return_on_equity <= 15:
                text_ReturnOnEquity = "Moderated - Potential but Need Improvements"
            elif return_on_equity <= 20:
                text_ReturnOnEquity = "Healthy - Efficient and Solid Management"
            else:
                text_ReturnOnEquity = "Good - Highly Efficient in Generating Profits"

        self._set_eval(evaluated_metrics, "ReturnOnEquity", text_ReturnOnEquity)

        # Return On Equity Growth
        return_on_equity_cagr = fm.safe_round(metrics.get('ratios', {}).get("ReturnOnEquityCAGR"))
        evaluated_metrics["ReturnOnEquityCAGR"] = return_on_equity_cagr if return_on_equity_cagr is not None else None

        if return_on_equity_cagr is None or math.isnan(return_on_equity_cagr):
            text_ReturnOnEquityCAGR = "No Data"
        else:
            if return_on_equity_cagr <= 0:
                text_ReturnOnEquityCAGR = "Not Good - No Growth or Negative Trend"
            else:
                text_ReturnOnEquityCAGR = "Good - Consistent Growth in Equity Returns"

        self._set_eval(evaluated_metrics, "ReturnOnEquityCAGR", text_ReturnOnEquityCAGR)

        return evaluated_metrics if evaluated_metrics else "Indefinido"
