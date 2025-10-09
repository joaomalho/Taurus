# app/services/yahoo.py
from backend.datasources.yahoodata import DataHistoryYahoo

# TTL de 30 min (ou o que quiseres)
dh = DataHistoryYahoo(ttl_minutes=30)
