from functools import lru_cache

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

BULLISH_THRESHOLD = 0.05
BEARISH_THRESHOLD = -0.05
DEFAULT_LIMIT = 30


@lru_cache(maxsize=1)
def _analyzer() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()


def label_from_compound(compound: float) -> str:
    if compound >= BULLISH_THRESHOLD:
        return "Bullish"
    if compound <= BEARISH_THRESHOLD:
        return "Bearish"
    return "Neutral"


def _pick_best_image(content: dict) -> str | None:
    thumbnail = content.get("thumbnail") or {}
    resolutions = thumbnail.get("resolutions") or []
    valid = [row for row in resolutions if isinstance(row, dict) and row.get("url")]
    if valid:
        best = max(valid, key=lambda row: row.get("width") or 0)
        return best.get("url")
    return thumbnail.get("originalUrl")


def normalize_yahoo_news_item(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raw = {}

    content = raw.get("content") or {}
    if not isinstance(content, dict):
        content = {}

    related = []
    storyline = content.get("storyline") or {}
    for entry in (storyline.get("storylineItems") if isinstance(storyline, dict) else None) or []:
        related_content = entry.get("content") if isinstance(entry, dict) else None
        if not isinstance(related_content, dict):
            continue
        related.append({
            "id": related_content.get("id"),
            "title": related_content.get("title") or "",
            "url": (
                (related_content.get("clickThroughUrl") or {}).get("url")
                or (related_content.get("canonicalUrl") or {}).get("url")
                or related_content.get("previewUrl")
                or "#"
            ),
            "type": related_content.get("contentType"),
            "image": _pick_best_image(related_content),
        })

    finance = content.get("finance") or {}
    premium_finance = finance.get("premiumFinance") if isinstance(finance, dict) else None
    if not isinstance(premium_finance, dict):
        premium_finance = {}

    return {
        "id": raw.get("id") or content.get("id"),
        "title": content.get("title") or "",
        "summary": content.get("summary") or "",
        "provider": (content.get("provider") or {}).get("displayName") or "Fonte",
        "url": (
            (content.get("clickThroughUrl") or {}).get("url")
            or (content.get("canonicalUrl") or {}).get("url")
            or content.get("previewUrl")
            or "#"
        ),
        "publishedAt": content.get("displayTime") or content.get("pubDate"),
        "isEditorsPick": bool((content.get("metadata") or {}).get("editorsPick")),
        "isPremium": bool(premium_finance.get("isPremiumNews")),
        "imageUrl": _pick_best_image(content),
        "contentType": content.get("contentType") or "STORY",
        "related": related,
    }


def score_text(text: str) -> dict:
    cleaned = (text or "").strip()
    if not cleaned:
        return {
            "compound": 0.0,
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 1.0,
            "label": "Neutral",
        }

    scores = _analyzer().polarity_scores(cleaned)
    compound = round(float(scores["compound"]), 4)
    return {
        "compound": compound,
        "positive": round(float(scores["pos"]), 4),
        "negative": round(float(scores["neg"]), 4),
        "neutral": round(float(scores["neu"]), 4),
        "label": label_from_compound(compound),
    }


def score_news_item(item: dict) -> dict:
    parts = [item.get("title") or "", item.get("summary") or ""]
    text = ". ".join(part.strip() for part in parts if part and part.strip())
    sentiment = score_text(text)
    return {**item, "sentiment": sentiment}


def build_sentiment_aggregate(items: list[dict]) -> dict:
    scored = [item["sentiment"]["compound"] for item in items if item.get("sentiment")]
    if not scored:
        return {
            "label": "Neutral",
            "compound_avg": 0.0,
            "positive_pct": 0.0,
            "neutral_pct": 0.0,
            "negative_pct": 0.0,
            "sample_size": 0,
        }

    compound_avg = round(sum(scored) / len(scored), 4)
    labels = [item["sentiment"]["label"] for item in items if item.get("sentiment")]
    positive_pct = round(labels.count("Bullish") / len(labels) * 100, 1)
    negative_pct = round(labels.count("Bearish") / len(labels) * 100, 1)
    neutral_pct = round(labels.count("Neutral") / len(labels) * 100, 1)

    return {
        "label": label_from_compound(compound_avg),
        "compound_avg": compound_avg,
        "positive_pct": positive_pct,
        "neutral_pct": neutral_pct,
        "negative_pct": negative_pct,
        "sample_size": len(scored),
    }


def analyze_news(raw_items: list | None, *, limit: int = DEFAULT_LIMIT) -> dict:
    if not raw_items:
        return {"items": [], "aggregate": build_sentiment_aggregate([])}

    normalized = [normalize_yahoo_news_item(raw) for raw in raw_items[:limit]]
    items = [score_news_item(item) for item in normalized if item.get("title")]
    return {
        "items": items,
        "aggregate": build_sentiment_aggregate(items),
    }
