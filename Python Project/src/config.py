from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Création des dossiers
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Facteur d'annualisation (252 car indexé sur Jours Ouvrés TradFi)
ANNUALIZATION_FACTOR = 252

# Paramètres temporels
START_DATE = "2021-01-01"
END_DATE = "2025-12-31"

# Tickers
BTC_SYMBOL = "BTCUSDT"
SPX_TICKER = "^GSPC"
VIX_TICKER = "^VIX"

# Standardisation des colonnes OHLCV
COLUMNS_OHLCV = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'symbol', 'source']