# News sentiment

Headline-level sentiment for Yahoo Finance news using [VADER](https://github.com/cjhutto/vaderSentiment) (Valence Aware Dictionary and sEntiment Reasoner).

## What it does

- Scores each headline (+ summary when available) as **Bullish**, **Neutral**, or **Bearish**
- Aggregates the last ~30 articles into an average compound score
- Feeds a small bias into the **investment verdict** (when at least 3 headlines are available)
- Shows per-article badges and a summary banner on the stock page

## Thresholds

| Compound score | Label |
|----------------|-------|
| ≥ 0.05 | Bullish |
| ≤ −0.05 | Bearish |
| otherwise | Neutral |

Compound scores range from −1 (most negative) to +1 (most positive).

## API

Sentiment is included automatically in:

| Endpoint | Field |
|----------|-------|
| `GET /stock/<symbol>/news/` | `items[].sentiment`, `sentiment` (aggregate) |
| `GET /stock/<symbol>/summary/` | `news.items`, `news.sentiment` |

### Aggregate example

```json
{
  "label": "Bullish",
  "compound_avg": 0.214,
  "positive_pct": 45.0,
  "neutral_pct": 35.0,
  "negative_pct": 20.0,
  "sample_size": 20
}
```

## Verdict integration

News sentiment contributes up to **±0.15** to the combined verdict score (soft signal). It appears in verdict reasons when enough headlines exist.

## Limitations

- Lexicon-based NLP — not a fine-tuned finance model
- English headlines work best; other languages may be less accurate
- Headlines alone can miss context from full articles
- Advisory only — not a trading signal on its own

## Dependency

`vaderSentiment` in `requirements.txt`. Rebuild Docker after pulling:

```bash
docker compose build web
docker compose up -d
```
