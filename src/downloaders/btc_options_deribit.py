"""
Module pour télécharger l'historique complet de l'indice DVOL (Deribit Volatility).
Implémentation selon la Solution A (approche macro/VIX).
"""

import logging
import requests
import pandas as pd
from datetime import datetime, timezone
import time

try:
    from src.config import DATA_DIR, START_DATE, END_DATE
except ImportError:
    from pathlib import Path
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    START_DATE = "2021-01-01"
    END_DATE = "2025-12-31"

logger = logging.getLogger(__name__)

DERIBIT_DVOL_API = "https://deribit.com/api/v2/public/get_volatility_index_data"

class DeribitDVOLDownloader:
    def __init__(self, currency="BTC"):
        self.currency = currency
        self.url = DERIBIT_DVOL_API

    def fetch_historical_dvol(self, start_date: str, end_date: str, resolution="1D", retries=3):
        start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now_dt = datetime.now(timezone.utc)
        if end_dt > now_dt: end_dt = now_dt
        end_ts = int(end_dt.timestamp() * 1000)

        all_candles = []
        current_start_ts = start_ts
        
        while current_start_ts < end_ts:
            # On demande des tranches de 900 jours max (l'API limite à 1000)
            chunk_end_ts = min(current_start_ts + (900 * 24 * 3600 * 1000), end_ts)
            
            params = {
                "currency": self.currency,
                "start_timestamp": current_start_ts,
                "end_timestamp": chunk_end_ts,
                "resolution": resolution
            }
            
            for attempt in range(retries):
                try:
                    response = requests.get(self.url, params=params, timeout=15)
                    response.raise_for_status()
                    data = response.json()
                    
                    if "result" in data and "data" in data["result"]:
                        candles = data["result"]["data"]
                        if candles:
                            all_candles.extend(candles)
                        
                        current_start_ts = chunk_end_ts + 1
                        time.sleep(0.5) 
                        break 
                    else:
                        logger.error("Erreur API.")
                        return all_candles
                except requests.RequestException:
                    time.sleep(2)
            else:
                return all_candles 
                
        return all_candles

    def process_and_save(self, raw_candles):
        if not raw_candles: return
        df = pd.DataFrame(raw_candles, columns=["timestamp_ms", "open", "high", "low", "close"])
        df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
        df["source"] = "deribit_dvol"
        df["symbol"] = f"{self.currency}_DVOL"
        df = df[["date", "open", "high", "low", "close", "symbol", "source"]]
        file_path = DATA_DIR / f"{self.currency.lower()}_dvol_historical.csv"
        df.to_csv(file_path, index=False)
        print(f"✅ Historique téléchargé ! Sauvegardé dans : {file_path}")

    def run(self):
        raw_candles = self.fetch_historical_dvol(start_date=START_DATE, end_date=END_DATE, resolution="1D")
        self.process_and_save(raw_candles)

if __name__ == "__main__":
    downloader = DeribitDVOLDownloader(currency="BTC")
    downloader.run()
