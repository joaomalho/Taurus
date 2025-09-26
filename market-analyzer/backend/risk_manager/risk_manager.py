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
            (1.0,        "Not Good (In Debt)",                "bad"),
            (1.5,        "Tight Margin to Debt",              "neutral"),
            (2.0,        "Good Debt Coverage",                "good"),
            (math.inf,   "Perfect Coverage (Double +)",       "verygood"),
        ],
        "QuickRatio": [
            (0.8,        "Not Good (In Debt)",                "bad"),
            (1.0,        "Tight Margin to Debt",              "neutral"),
            (1.5,        "Good Debt Coverage",                "good"),
            (math.inf,   "Perfect Coverage (Double +)",       "verygood"),
        ],
        "EnterpriseFCFYield": [
            (2.5,        "Expensive",                         "bad"),
            (4.0,        "Fair",                              "neutral"),
            (math.inf,   "Cheap",                             "verygood"),
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
        "EquityFCFYield": {
            "verygood": lambda v: {
                "short":  f"**Equity FCF Yield =** {v:.2f}%",
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
                "short":  f"**Equity FCF Yield =** {v:.2f}%",
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
                "short":  f"**Equity FCF Yield =** {v:.2f}%",
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
        # usa o bucket vindo das regras em vez de inferir por substring
        # (mantemos compatibilidade: se vier um texto diferente, cai em neutral)
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
        out[f"{key}_bucket"] = bucket                # define o bucket antes
        self._set_eval(out, key, evaluation)         # mantém chaves/cores existentes
        for k, v in (msgs or {}).items():
            self._set_message(out, key, k, v)

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

        evaluated_metrics["trailingPE"] = trailing_pe if trailing_pe is not None else None
        evaluated_metrics["sectorTrailingPE"] = sector_pe if sector_pe is not None else None
        evaluated_metrics["forwardPE"] = forward_pe if forward_pe is not None else None

        # Só avalia o score se TODOS estiverem presentes
        if None not in (trailing_pe, sector_pe, forward_pe):
            score_pe = 0
            score_pe += 1 if trailing_pe < sector_pe else -1 if trailing_pe > sector_pe else 0
            score_pe += 1 if forward_pe < sector_pe else -1 if forward_pe > sector_pe else 0
            score_pe += 1 if trailing_pe > forward_pe else -1 if trailing_pe < forward_pe else 0

            text_trailingPE = {
                3:  "Very Low Undervalued",
                2:  "Low Undervalued",
                1:  "Undervalued",
                0:  "Neutral Valued",
                -1: "Overvalued",
                -2: "High Overvalued",
            }.get(score_pe, "Very High Overvalued")
        else:
            text_trailingPE = "No Data"

        self._set_eval(evaluated_metrics, "trailingPE", text_trailingPE)

        # ----- EV / EBITDA
        ev_ebitda = fm.safe_round(kpis.get("evEbitda"))
        evaluated_metrics["evEbitda"] = ev_ebitda if ev_ebitda is not None else None
        if ev_ebitda is None:
            text_ev_ebitda = "No Data"
        else:
            if ev_ebitda <= 8:
                text_ev_ebitda = "Cheap"
            elif ev_ebitda <= 12:
                text_ev_ebitda = "Fair"
            else:
                text_ev_ebitda = "Expensive"

        self._set_eval(evaluated_metrics, "evEbitda", text_ev_ebitda)

        # ----- Prise To Sale
        price_to_sale = fm.safe_round(kpis.get("PriceToSale"))

        evaluated_metrics["PriceToSale"] = price_to_sale if price_to_sale is not None else None

        if price_to_sale is None:
            text_price_to_sale = "No Data"
        else:
            if price_to_sale <= 2:
                text_price_to_sale = "Cheap"
            elif price_to_sale <= 6:
                text_price_to_sale = "Fair"
            else:
                text_price_to_sale = "Expensive"

        self._set_eval(evaluated_metrics, "PriceToSale", text_price_to_sale)

        # ----- Equity FCF Yield
        equity_fcf_yield = fm.safe_round(kpis.get("EquityFCFYield"))
        evaluated_metrics["EquityFCFYield"] = equity_fcf_yield if equity_fcf_yield is not None else None
        if equity_fcf_yield is None:
            text_equity_fcf_yield = "No Data"
        else:
            if equity_fcf_yield <= 3:
                text_equity_fcf_yield = "Expensive"
            elif equity_fcf_yield <= 5:
                text_equity_fcf_yield = "Fair"
            else:
                text_equity_fcf_yield = "Cheap"

        self._set_eval(evaluated_metrics, "EquityFCFYield", text_equity_fcf_yield)

        # ----- Enterprise FCF Yield
        efy = fm.safe_round(kpis.get("EnterpriseFCFYield"))
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
