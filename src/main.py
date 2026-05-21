from src.downloaders.btc_spot_binance import download_btc_spot
from src.downloaders.spx_spot_yfinance import download_yfinance_data
from src.downloaders.btc_options_deribit import DeribitDVOLDownloader
from src.config import SPX_TICKER, VIX_TICKER

def main():
    print("Démarrage de la pipeline de données (Thèse MACRO)...")
    
    # 1. BTC Spot
    download_btc_spot()
    
    # 2. SPX
    download_yfinance_data(SPX_TICKER, "spx_daily_yfinance.csv", "^GSPC")
    
    # 3. VIX
    download_yfinance_data(VIX_TICKER, "vix_daily_yfinance.csv", "^VIX")
    
    # 4. BTC DVOL
    print("--- Téléchargement Historique BTC DVOL (macro options) ---")
    dvol_downloader = DeribitDVOLDownloader(currency="BTC")
    dvol_downloader.run()
    
    print("Terminé ! Toutes tes données pour l'analyse sont prêtes.")

if __name__ == "__main__":
    main()