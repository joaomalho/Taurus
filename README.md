
![Logo](https://github.com/joaomalho/Taurus/blob/main/images/taurus.png?raw=true)


This tool analyzes finantial markets in real time to help investors.




## Autores

[@joaomalho](https://github.com/joaomalho)


## Licença

[MIT](https://choosealicense.com/licenses/mit/)


## Roadmap

- Continuação de migração da ferramenta desenvolvida localmente.
- Funções de coleta de informação - Yahooo (Done) 

## Last updates

Use of Parallelization through Joblib to optimization process of :
* Crossover
* Bollinger Bands
* RSI - Missing

Replace of hardcoded funcions by TA-Lib.
* Trend Metrics `trend_metrics`

New measures of to valuate strategies performance:
* Sharpe Ratio
* Max Drawdown
* Expectancy

## Disclaimers

### Tipos de Dados e Delay Esperado

__Source:__ Yahoo Finance(yfifnance)

__Dados Intradiários (Intervalo Menor que 1 Dia):__

__Delay:__ Aproximadamente 1-2 minutos.
__Descrição:__ Os dados de intervalos menores (1 minuto, 5 minutos, etc.) são quase em tempo real, mas podem ter um pequeno atraso devido ao processamento e à frequência de atualização dos servidores do Yahoo Finance.
__Limitações:__ Nem todos os ativos suportam intervalos intradiários em mercados específicos.

__Dados Diários ou de Períodos Maiores:__

__Delay:__ Normalmente o mesmo dia ou no próximo dia útil (atualizado ao fim do pregão).
__Descrição:__ Os dados diários são amplamente confiáveis e usados para análise histórica ou estratégias de longo prazo.

__Dados de Moedas (Forex):__

__Delay:__ Varia de 15 segundos a 1 minuto.
__Descrição:__ Dados cambiais geralmente têm menos atraso porque são derivados de fontes que atualizam com maior frequência.

__Dados de Ações e ETFs:__

__Delay:__ Pode ser entre 15 segundos a 2 minutos, dependendo da troca (exchange).
__Descrição:__ Algumas bolsas impõem atrasos para acesso gratuito, o que se reflete no yfinance.

__Dados de Criptomoedas:__

__Delay:__ Aproximadamente 1-2 minutos.
__Descrição:__ Criptomoedas são frequentemente atualizadas, mas não são tão rápidas quanto APIs dedicadas, como a Binance ou Coinbase.

