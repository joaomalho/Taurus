from celery import shared_task

from frontend_app.services.screener_cache import refresh_all_screeners, refresh_screener


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_screener_task(self, name: str):
    try:
        df = refresh_screener(name)
        return {"screener": name, "rows": 0 if df is None else len(df)}
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_all_screeners_task(self):
    try:
        return refresh_all_screeners()
    except Exception as exc:
        raise self.retry(exc=exc)
