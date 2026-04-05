import pandas as pd
import yfinance as yf
import datetime
import time
import requests
from requests.exceptions import RequestException
import traceback

# pip install pandas yfinance
# pip install -U yfinance
# pip show yfinance


# Définition des principaux indices par pays
indices = {
    # "MY-LIST": "^MINE"
    "FRANCE": ["^FCHI", "^ALASI.PA"],    # CAC 40, EuroNext Growth
    # "ETATS-UNIS": ["^DJI", "^GSPC", "^IXIC"],  # Dow Jones, S&P 500, NASDAQ
    # "JAPON": "^N225",     # Nikkei 225
    # "CHINE": ["^SSEC", "^HSI"],  # Shanghai Composite, Hang Seng
    # "SUISSE": "^SSMI"     # Swiss Market Index
}

# Fonction pour obtenir les composants d'un indice
def get_index_components(index_ticker):
    """
    Récupère les composants d'un indice boursier donné.
    
    Args:
        index_ticker (str): Le symbole de l'indice boursier
        
    Returns:
        list: Liste des symboles correspondant aux composants de l'indice
    """
    if index_ticker == "^FCHI":  # CAC 40
        return ["AI.PA", "MC.PA", "OR.PA", "SAN.PA", "BN.PA", "CS.PA", "KER.PA", "ML.PA", "AIR.PA", "RI.PA",
                "VIE.PA", "EN.PA", "LR.PA", "CA.PA", "HO.PA", "DG.PA", "SW.PA", "ORA.PA", "ACA.PA", "UG.PA",
                "BNP.PA", "GLE.PA", "RMS.PA", "AC.PA", "FR.PA", "CAP.PA", "STM.PA", "SGO.PA", "SU.PA", "EL.PA",
                "DSY.PA", "ENGI.PA", "TTE.PA", "VIV.PA", "WLN.PA", "ERF.PA", "MT.AS", "VCT.PA"]
    elif index_ticker == "^ALASI.PA": # EuroNext Growth
        return ["ALALO.PA15", "ALARF.PA", "ADOM.PA", "ALAGP.PA", "81E.F", "ALORA.PA", "ALAQU.PA", "ALCUR.PA", 
                "AAN.V", "ALAMG.PA", "ALBAI.PA", "ALBDM.PA", "ALBER.PA", "ALBLD.PA", "ALBIO.PA", "ALBPS.PA", 
                "ALBIO.PA", "ALTBG.PA", "ALBLU.PA", "ALBOU.PA", "ALBRO.PA", "ALCAN.PA", "ALCAR.PA", "ALCAR.PA", 
                "ALCLS.PA", "ALCER.PA", "ALCFD.PA", "ALCGR.PA", "ALCOI.PA", "ALCRO.PA", "ALCYB.PA", "ALDLS.PA", 
                "ALDAM.PA", "ALDBT.PA", "ALDEL.PA", "ALDEV.PA", "ALDNX.PA", "ALDOL.PA", "ALDON.PA", "ALDON.PA", 
                "ALDRV.PA", "ALECO.PA", "ALEDI.PA", "ALEMO.PA", "ALENC.PA", "ALENE.PA", "ALENT.PA", "ALEPR.PA", 
                "ALEO2.PA", "ALEUR.PA", "ALEBS.PA", "ALEFC.PA ", "ALEMD.PA", "ALEUP.PA", "ALFBA.PA", "ALFDT.PA", 
                "ALFPA.PA", "ALFRE.PA", "ALGAS.PA", "ALGEN.PA", "ALGEV.PA", "ALGBE.PA", "ALGBG.PA", "ALGWM.PA", 
                "ALGRE.PA", "ALGUI.PA", "ALTER.PA", "ALGPI.PA", "ALHER.PA", "ALHIT.PA", "ALHOC.PA", "ALICE.PA", 
                "ALI2S.PA", "ALIDS.PA", "ALIMM.PA", "ALIMP.PA", "ALING.PA", "ALINS.PA", "ALINV.PA", "ALISD.PA", 
                "ALKAL.PA", "ALKER.PA", "ALKKO.PA", "ALKLA.PA", "ALKLE.PA", "ALLAN.PA", "ALLDC.PA", "ALLHB.PA", 
                "ALLXB.PA", "ALLMA.PA", "ALLLE.PA", "ALLOG.PA", "ALLUC.PA", "ALMII.PA", "ALMLC.PA", "ALMAR.PA", 
                "ALMAS.PA", "ALMDT.PA", "ALMET.PA", "ALMGI.PA", "ALMGD.PA", "ALMLB.PA", "ALMIN.PA", "ALMNT.PA", 
                "ALMOL.PA", "ALMOU.PA", "ALMUN.PA", "ALNEO.PA", "ALNEV.PA", "ALNET.PA", "ALNXT.PA", "ALNOV.PA", 
                "ALNSC.PA", "ALNSE.PA", "ALORD.PA", "ALORI.PA", "ALOVO.PA", "ALPAU.PA", "ALPID.PA", "ALPAT.PA", 
                "ALPOU.PA", "ALPOL.PA", "ALPRE.PA", "ALPRI.PA", "ALPRO.PA", "ALPUL.PA", "ALQGC.PA", "ALQWA.PA", 
                "ALREA.PA", "ALREW.PA", "ALROC.PA", "ALROU.PA", "ALSAF.PA", "ALSPM.PA", "ALSEN.PA", "ALSTD.PA", 
                "ALSTM.PA", "ALSEI.PA", "ALSOF.PA", "ALSTH.PA", "ALSGD.PA", "ALSPW.PA", "ALSTF.PA", "ALSTW.PA", 
                "ALTHC.PA", "ALTHX.PA", "ALTPM.PA", "ALTON.PA", "ALTRI.PA", "ALTRS.PA", "ALTXC.PA", "ALU10.PA", 
                "ALUNI.PA", "ALUPG.PA", "ALUVE.PA", "ALVAL.PA", "ALVUQ.PA", "ALVER.PA", "ALVIA.PA", "ALVOG.PA", 
                "ALVMD.PA", "ALWGX.PA", "ALWEC.PA", "ALWST.PA", "ALWIT.PA"]
    elif index_ticker == "^DJI":  # Dow Jones
        return ["AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW", "GS", "HD", "HON", "IBM", "INTC",
                "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"]
    elif index_ticker == "^GSPC":  # S&P 500 (complet)
        # Liste complète des composants du S&P 500
        sp500_tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", 
                            "TSLA", "UNH", "BRK-B", "JPM", "JNJ", "V", "PG", "XOM", 
                            "MA", "LLY", "HD", "AVGO", "BAC", "CVX", "MRK", "KO", "PEP", 
                            "COST", "ABBV", "PFE", "WMT", "TMO", "ADBE", "CSCO", "DIS", 
                            "ACN", "CRM", "ABT", "MCD", "AMD", "SPGI", "CMCSA", "NFLX", 
                            "PM", "TXN", "DHR", "HON", "WFC", "INTC", "QCOM", "RTX", "CAT", 
                            "AMGN", "IBM", "UPS", "BMY", "DE", "NKE", "GE", "LIN", "INTU", 
                            "MDLZ", "BA", "BKNG", "TJX", "LOW", "SCHW", "AXP", "SBUX", "MMM", 
                            "MS", "ADI", "GS", "VRTX", "AMT", "ISRG", "ELV", "BLK", "GILD", 
                            "ADP", "SYK", "NOW", "MO", "PLD", "ZTS", "C", "REGN", "CI", "PANW", 
                            "AMAT", "SO", "TMUS", "FI", "ITW", "CB", "TGT", "CME", "PGR", "BX", 
                            "BSX", "APD", "DUK", "EQIX", "ETN", "CL", "EOG", "CCI", "GD", "ORLY", 
                            "MU", "CSX", "USB", "MDT", "SNPS", "SLB", "PXD", "SHW", "AON", "ICE", 
                            "NOC", "EMR", "MCK", "HUM", "MAR", "CDNS", "LRCX", "MPC", "EL", "PSA", 
                            "TT", "NSC", "MMC", "GIS", "AEP", "A", "FDX", "WM", "F", "FTNT", "ADM", 
                            "HSY", "HCA", "SRE", "DXCM", "TFC", "ECL", "MNST", "APH", "D", "ROP", 
                            "TDG", "ITW", "WMB", "TEL", "KLAC", "PH", "BIIB", "MSI", "ADSK", "CTAS", 
                            "PCAR", "EA", "IDXX", "MTD", "O", "URI", "MRNA", "NXPI", "RSG", "SPG", 
                            "FCX", "ROK", "BK", "FIS", "MSCI", "HLT", "YUM", "CMG", "CHTR", "MET", 
                            "PNC", "KMB", "CTSH", "PAYX", "PPG", "AIG", "SYY", "ED", "WELL", "AJG", 
                            "DVN", "VRSK", "ESS", "ILMN", "KDP", "WEC", "VMC", "DFS", "DG", "AFL", 
                            "STZ", "IR", "WST", "CNC", "ALGN", "DD", "LHX", "GL", "HPQ", "DOW", "DOV", 
                            "BNS", "XEL", "ROST", "OTIS", "ANET", "CPRT", "EXC", "ANSS", "EIX", "STT", 
                            "KR", "IQV", "MTB", "TDY", "VLO", "FAST", "ALL", "PPL", "AWK", "ODFL", "LVS", 
                            "DLTR", "SBAC", "GLW", "KEYS", "CPB", "WTW", "GEHC", "WBA", "HAL", "ALB", 
                            "GWW", "MPWR", "VICI", "PEG", "APTV", "RMD", "DLR", "WY", "RCL", "LUV", 
                            "NEM", "RF", "BCE", "HBAN", "IR", "XYL", "DTE", "TRV", "COF", "LEN", 
                            "WDAY", "KHC", "IP", "DRI", "CFG", "ETR", "DGX", "OKE", "AEE", "WAB", 
                            "CCL", "HIG", "AVB", "CHD", "EXR", "ULTA", "CDW", "MLM", "FTV", "DAL", 
                            "TSN", "PRU", "FE", "ZBH", "CRL", "K", "PCG", "BF-B", "WAT", "AMP", 
                            "DASH", "HST", "BAX", "SWK", "PWR", "EXPD", "HOLX", "NVR", "MKC", 
                            "ATO", "GPC", "ROL", "FICO", "UAL", "TXT", "STE", "CLX", "BALL", 
                            "LH", "EXPE", "OMC", "CE", "AAL", "OGN", "BWA", "MAS", "VTR", 
                            "FDS", "J", "MTG", "BBWI", "EFX", "CINF", "RJF", "ALK", "TYL", 
                            "NRG", "WRB", "BRO", "CMS", "CAH", "WBD", "PTC", "CTRA", "TRGP", 
                            "BBY", "LYB", "L", "PAYC", "CTVA", "AXON", "CHRW", "FANG", "BLDR", 
                            "PKI", "HWM", "CNP", "INVH", "FOXA", "VFC", "GEN", "KMX", "NTAP", 
                            "AKAM", "SNA", "JBHT", "ES", "BIO", "DHI", "HPE", "TER", "RE", 
                            "JKHY", "HRL", "IFF", "UAA", "UA"]
        return sp500_tickers
    elif index_ticker == "^IXIC":  # NASDAQ (retournant principales)
        return ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "ASML",
                "ADBE", "COST", "PEP", "CSCO", "NFLX", "CMCSA", "AMD", "INTC", "TMUS", "QCOM", "AMAT"]
    elif index_ticker == "^N225":  # Nikkei 225 (principales)
        return ["7203.T", "9984.T", "6758.T", "8035.T", "6861.T", "6501.T", "6902.T", "6594.T",
                "9432.T", "8058.T", "4063.T", "4519.T", "8031.T", "9433.T", "7974.T", "9983.T"]
    elif index_ticker == "^SSEC":  # Shanghai Composite (principales)
        return ["600519.SS", "601318.SS", "600036.SS", "601398.SS", "600000.SS",
                "601288.SS", "600050.SS", "601668.SS", "601988.SS"]
    elif index_ticker == "^HSI":  # Hang Seng (principales)
        return ["0700.HK", "0941.HK", "9988.HK", "0939.HK", "1299.HK", "2318.HK",
                "0005.HK", "1398.HK", "0388.HK", "2388.HK"]
    elif index_ticker == "^SSMI":  # Swiss Market Index
        return ["NESN.SW", "ROG.SW", "NOVN.SW", "UHR.SW", "ABB.SW", "SLHN.SW", "SIKA.SW",
                "LONN.SW", "ZURN.SW", "CFR.SW", "GIVN.SW", "SCMN.SW", "SREN.SW", "GEBN.SW",
                "CSGN.SW", "KNIN.SW", "HOLN.SW", "UBSG.SW", "PGHN.SW"]
    elif index_ticker == "^MINE":  # My personal list
        return ["ALTBG.PA", "ALJXR.PA", "74SW.PA"]
    else:
        return []
    

def get_stocks_near_ma200(retry_count=3):
    """
    Cette fonction identifie les entreprises des principaux indices de France, États-Unis, Japon,
    Chine et Suisse dont le cours de bourse est proche de leur moyenne mobile à 200 jours
    (entre -1% et +3%).
    
    Args:
        retry_count (int): Nombre de tentatives pour chaque requête API en cas d'échec
    
    Returns:
        DataFrame: Liste triée des entreprises respectant le critère, avec leur écart par rapport à la MA200
    """
    
    # Création de la liste pour stocker les résultats
    results = []
    today = datetime.datetime.now()
    one_year_ago = today - datetime.timedelta(days=365)
    
    # Pour chaque pays et ses indices
    for serie, serie_indices in indices.items():
        if not isinstance(serie_indices, list):
            serie_indices = [serie_indices]
        
        print(f"\nAnalyse des indices pour {serie}...")
        
        for index_ticker in serie_indices:
            print(f"Récupération des composants pour l'indice {index_ticker}...")
            tickers = get_index_components(index_ticker)
            print(f"Nombre d'entreprises à analyser: {len(tickers)}")
            
            for ticker_symbol in tickers:
                try:
                    # Création d'un objet Ticker pour chaque symbole
                    print(f"Traitement de {ticker_symbol}...")
                    ticker = yf.Ticker(ticker_symbol)
                    
                    # Téléchargement des données historiques avec gestion d'erreurs et retry
                    retry_attempts = 0
                    success = False
                    
                    while not success and retry_attempts < retry_count:
                        try:
                            data = ticker.history(period="1y")
                            success = True
                        except (RequestException, ValueError) as e:
                            retry_attempts += 1
                            print(f"Tentative {retry_attempts}/{retry_count} échouée pour {ticker_symbol}: {e}")
                            if retry_attempts < retry_count:
                                time.sleep(1)  # Attente plus longue entre les tentatives
                            else:
                                print(f"Échec après {retry_count} tentatives pour {ticker_symbol}")
                                raise
                    
                    if data.empty or len(data) < 200:
                        print(f"Données insuffisantes pour {ticker_symbol}, minimum 200 jours requis")
                        continue
                        
                    # Récupération du nom de l'entreprise
                    try:
                        company_name = ticker.info.get('shortName', ticker_symbol)
                    except:
                        company_name = ticker_symbol
                    
                    # Calcul de la moyenne mobile à 200 jours
                    data['MA200'] = data['Close'].rolling(window=200).mean()
                    
                    # Récupération du dernier cours et de la dernière MA200
                    last_close = data['Close'].iloc[-1]
                    last_ma200 = data['MA200'].iloc[-1]
                    
                    if pd.isna(last_ma200):
                        print(f"Moyenne mobile à 200 jours non disponible pour {ticker_symbol}")
                        continue
                    
                    # Calcul de l'écart en pourcentage
                    percentage_diff = ((last_close - last_ma200) / last_ma200) * 100
                    
                    # Vérification si l'écart est dans la plage souhaitée (-1% à +3%)
                    if -1 <= percentage_diff <= 3:
                        print(f"✓ {ticker_symbol} ({company_name}) - Écart: {percentage_diff:.2f}%")
                        results.append({
                            'Ticker': ticker_symbol,
                            'Nom': company_name,
                            'Pays': serie,
                            'Dernier_Cours': last_close,
                            'MA200': last_ma200,
                            'Écart_Pourcentage': percentage_diff
                        })
                    
                except Exception as e:
                    print(f"Erreur lors du traitement de {ticker_symbol}: {e}")
                    print(f"Erreur lors du téléchargement des données pour {ticker_symbol}: {e}")
                
                # Pause pour éviter de surcharger l'API
                time.sleep(0.5)
    
    # Création d'un DataFrame à partir des résultats
    if results:
        df_results = pd.DataFrame(results)
        
        # Tri par écart décroissant
        df_results = df_results.sort_values(by='Écart_Pourcentage', ascending=False)
        
        return df_results
    else:
        return pd.DataFrame()

def get_stocks_near_ma200_to_CSV():
    """
    Cette fonction identifie les entreprises d'une série dont le cours de bourse est proche de leur moyenne mobile à 200 jours
    (entre -1% et +3%) et renvoie le résultat au format CSV.
    
    """
    print("Recherche des actions proches de leur moyenne mobile à 200 jours...")
    print("Analyse de tous les composants des indices majeurs (CAC40, S&P500 complet, Dow Jones, NASDAQ, Nikkei, etc.)")
    print("Ce processus peut prendre plusieurs minutes en raison du grand nombre d'actions à analyser...")
    
    results = get_stocks_near_ma200()
    
    if not results.empty:
        print(f"\nRésultats ({len(results)} entreprises trouvées):")
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 120)
        print(results)
        
        # Résumé par pays
        print("\nRépartition par pays:")
        country_counts = results['Pays'].value_counts()
        for country, count in country_counts.items():
            print(f"{country}: {count} entreprises")
        
        # Exportation des résultats vers un fichier CSV
        csv_filename = f'actions_proches_ma200_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
        results.to_csv(csv_filename, index=False)
        print(f"\nLes résultats ont été exportés dans '{csv_filename}'")
    else:
        print("Aucune entreprise ne correspond aux critères.")


def get_stocks_with_momentum(retry_count=3):
    """
    Cette fonction identifie les entreprises des principaux indices de France, États-Unis, Japon,
    Chine et Suisse dont la tendance du cours de bourse peut etre qualifié de momentum.
    
    Args:
        retry_count (int): Nombre de tentatives pour chaque requête API en cas d'échec
    
    Returns:
        DataFrame: Liste triée des entreprises respectant le critère, avec leur écart par rapport à la MA200
    """
    
    # Création de la liste pour stocker les résultats
    results = []
    window = 12
    today = datetime.datetime.now()
    one_year_ago = today - datetime.timedelta(days=365)
    
    # Pour chaque pays et ses indices
    for serie, serie_indices in indices.items():
        if not isinstance(serie_indices, list):
            serie_indices = [serie_indices]
        
        print(f"\nAnalyse des indices pour {serie}...")
        
        for index_ticker in serie_indices:
            print(f"Récupération des composants pour l'indice {index_ticker}...")
            tickers = get_index_components(index_ticker)
            print(f"Nombre d'entreprises à analyser: {len(tickers)}")
            
            for ticker_symbol in tickers:
                result = analyze_momentum(ticker_symbol, window)

                if "error" in result:
                    print(f"Erreur: {result['error']}")
                    return
                
                print(f"\nAnalyse de momentum pour {ticker_symbol} (période de {window} jours):")
                print("-" * 50)
                
                if result["has_momentum"]:
                    print(f"🔍 Un momentum {result['momentum_direction']} a été détecté.")
                    print(f"💪 Force du momentum: {result['momentum_strength']:.2f}")
                else:
                    print(f"🔍 Pas de momentum significatif détecté.")
                    print(f"💪 Force du momentum: {result['momentum_strength']:.2f} (insuffisant)")
                
                # Afficher les données récentes
                recent_data = result["price_data"].tail(5)
                print("\nDonnées récentes:")
                print(recent_data[['Adj Close', 'return', 'ema', 'momentum_strength']].round(2))


def analyze_momentum(ticker, window=12, end_date=None):
    """
    Analyse si une action suit un phénomène de momentum sur une période de jours glissants.
    
    Args:
        ticker (str): Le symbole ticker Yahoo Finance de l'action à analyser.
        window (int, optional): La période de jours glissants pour calculer le momentum. Par défaut 12.
        end_date (str, optional): Date de fin de l'analyse au format 'YYYY-MM-DD'. Par défaut None (date actuelle).
    
    Returns:
        dict: Un dictionnaire contenant les résultats de l'analyse:
            - 'has_momentum': True si l'action suit un momentum, False sinon
            - 'momentum_strength': Force du momentum (score Z)
            - 'momentum_direction': Direction du momentum ('haussier' ou 'baissier')
            - 'price_data': DataFrame contenant les données de prix et les indicateurs de momentum
    """
    # Télécharger les données historiques
    start_date = None  # yfinance calculera automatiquement une période adaptée
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    try:
        # Récupérer l'historique des prix ajustés de clôture
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            return {"error": f"Pas de données disponibles pour le ticker {ticker}"}
        
        # S'assurer que nous avons assez de données
        if len(data) < window * 2:
            return {"error": f"Pas assez de données pour une analyse fiable (nécessite au moins {window*2} jours)"}
        
        # Calculer le rendement sur la période du momentum
        data['return'] = data['Close'].pct_change(window)

        
        # Calculer la moyenne mobile exponentielle du prix ajusté
        data['ema'] = data['Close'].ewm(span=window).mean()

        
        # Calculer l'écart par rapport à la moyenne mobile
        def calculate_diff(row):
            return row['Close'] - row['ema']
        
        data['price_ema_diff'] = data.apply(calculate_diff, axis=1)
        
        print(data['price_ema_diff'])

        # Calculer la force du momentum (Z-score du rendement sur la période)
        rolling_mean = data['return'].rolling(window=window).mean()
        rolling_std = data['return'].rolling(window=window).std()
        data['momentum_strength'] = (data['return'] - rolling_mean) / rolling_std
        
        # Déterminer si l'action suit un momentum
        # Critères:
        # 1. Rendement sur la période est positif/négatif
        # 2. Le prix est au-dessus/en-dessous de sa moyenne mobile exponentielle
        # 3. La force du momentum (Z-score) est significative (> 1 ou < -1)
        
        # Obtenir les dernières valeurs disponibles
        last_idx = data.dropna(subset=['momentum_strength']).index[-1]
        last_return = data.loc[last_idx, 'return']
        last_price_ema_diff = data.loc[last_idx, 'price_ema_diff']
        last_momentum_strength = data.loc[last_idx, 'momentum_strength']
        
        # Déterminer s'il y a un momentum et sa direction
        has_bullish_momentum = (last_return > 0 and 
                              last_price_ema_diff > 0 and 
                              last_momentum_strength > 1)
        
        has_bearish_momentum = (last_return < 0 and 
                              last_price_ema_diff < 0 and 
                              last_momentum_strength < -1)
        
        has_momentum = has_bullish_momentum or has_bearish_momentum
        
        momentum_direction = "haussier" if has_bullish_momentum else "baissier" if has_bearish_momentum else "neutre"
        
        # Préparer les résultats
        result = {
            "has_momentum": has_momentum,
            "momentum_strength": last_momentum_strength,
            "momentum_direction": momentum_direction,
            "price_data": data
        }
        
        return result
    
    except Exception as e:
        return {"error": f"Une erreur s'est produite: {str(e)}"}


def get_stocks_with_momentum_to_CSV():
    """
    Cette fonction identifie les entreprises d'une série dont le cours de bourse est sur une tendance momemtum 
    et renvoie le résultat au format CSV.
    
    """
    print("Recherche des actions proches de leur moyenne mobile à 200 jours...")
    print("Analyse de tous les composants des indices majeurs (CAC40, S&P500 complet, Dow Jones, NASDAQ, Nikkei, etc.)")
    print("Ce processus peut prendre plusieurs minutes en raison du grand nombre d'actions à analyser...")
    
    results = get_stocks_with_momentum()



##########################################################################
# FONCTIONS UTILITAIRES A RECOPIER
##########################################################################

#  💣  💥  🔥  📛  ⛔  ❌  🚫  ❗  ✅
#  🚧  🚨  💬
#  🌩  🌧  🌥
#  ⏰
#  📁  📄  📝  🔎
#  🔜  ⇢

def start_program() -> datetime:
    """
    Message de démarrage du programme, renvoie l'heure exacte de démarrage du programme\n

    Returns:
        datime.now()
    """

    print()
    print("🚀  momemtum-stocks.py is running")
    print()
    return datetime.datetime.now()


def menu() -> str:
    """
    Affiche un menu de sélection\n

    Returns:
        the user's prompt
    """

    print("1️⃣   Get all stocks near average 200 days")
    print("2️⃣   Is momemtum for the input")
    print("3️⃣   xxx")
    print("4️⃣   xxx")
    print()
    menu = input("⇢ Votre choix : ").strip()
    return menu

def end_program() -> datetime:
    """
    Message de fin du programme, renvoie l'heure exacte de fin du programme\n

    Returns:
        datime.now()
    """

    print()
    print()
    return datetime.datetime.now()

def print_executionTime(_start, _finish) -> datetime:
    """
    Mesure le temps écoulé entre deux dates et l'affiche en console\n

    Args:
        _start (datetime) : 1st date of the interval
        _finish (datetime) : 2nd date of the interval

    Returns:
        difference between ``_finish`` and ``_start``
    """

    print(f"⏰ {_finish - _start}")
    print()
    return _finish - _start


# FIN - FONCTIONS UTILITAIRES A RECOPIER
##########################################################################


if __name__ == '__main__':

    start = start_program()

    match menu():
        case "1":  
            get_stocks_near_ma200()
            
        case "2":
            analyze_momentum("AAPL", 12)
                
        case _:
            print("❌ ce choix n'existe pas")

    finish = end_program()
    print_executionTime(start, finish)

