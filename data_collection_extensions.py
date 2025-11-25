"""
Data Collection Extension Examples
===================================

This script shows how to integrate additional data sources into the 
Crypto Corruption Index application.

Add these functions to crypto_corruption_index.py or import them as a module.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============================================================================
# GEOGRAPHIC CRYPTO PREMIUMS
# ============================================================================

def fetch_p2p_premiums(countries: List[str] = None) -> pd.DataFrame:
    """
    Fetch P2P crypto premiums by country
    
    This would integrate with services like:
    - Paxful API
    - LocalBitcoins historical data
    - Binance P2P data
    
    Premium = (P2P price - spot price) / spot price
    
    High premiums indicate capital controls or banking restrictions
    """
    # Example structure - would need actual API integration
    
    if countries is None:
        countries = ['Argentina', 'Nigeria', 'Lebanon', 'Venezuela', 'Russia']
    
    # Placeholder - replace with actual API calls
    data = []
    for country in countries:
        # In production: fetch from Paxful/LocalBitcoins APIs
        premium = 0.05  # Example: 5% premium
        
        data.append({
            'country': country,
            'date': datetime.now(),
            'btc_premium_pct': premium,
            'volume_usd': 1000000,
            'trade_count': 150
        })
    
    return pd.DataFrame(data)


def fetch_kimchi_premium() -> pd.DataFrame:
    """
    Fetch the "Kimchi Premium" - price difference between Korean and US exchanges
    
    Historical indicator of capital controls
    When high = Koreans paying premium to move capital
    """
    # Would integrate with Korean exchange APIs (Upbit, Bithumb)
    # And compare to US exchanges (Coinbase, Kraken)
    
    # Placeholder structure
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    
    return pd.DataFrame({
        'date': dates,
        'korea_price': [45000 + i*10 for i in range(len(dates))],
        'us_price': [44000 + i*10 for i in range(len(dates))],
        'premium_pct': [2.0 + (i % 30)/10 for i in range(len(dates))],
        'volume_btc': [1000 + (i % 100)*10 for i in range(len(dates))]
    })


# ============================================================================
# SANCTIONS & POLICY DATA
# ============================================================================

def fetch_ofac_sanctions() -> pd.DataFrame:
    """
    Fetch OFAC sanctions list updates
    
    API: https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/
    
    Track additions to sanctioned entities list
    """
    # Example implementation
    
    url = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV"
    
    try:
        # In production, would parse the CSV and track changes over time
        df = pd.read_csv(url, encoding='latin1')
        
        # Count sanctions by country and date
        sanctions_by_country = df.groupby('Country').size().reset_index(name='count')
        
        return sanctions_by_country
    
    except Exception as e:
        print(f"Error fetching OFAC data: {e}")
        return pd.DataFrame()


def fetch_capital_control_events(sources: List[str] = None) -> pd.DataFrame:
    """
    Scrape capital control announcements from news sources
    
    Could use:
    - GDELT Project (global event database)
    - NewsAPI (news aggregation)
    - Central bank websites
    - IMF Article IV reports
    """
    # Placeholder structure
    
    events = [
        {
            'date': '2024-01-15',
            'country': 'Argentina',
            'event': 'Increased forex restrictions',
            'source': 'Central Bank announcement',
            'severity': 7
        },
        # In production: fetch from GDELT or NewsAPI
    ]
    
    return pd.DataFrame(events)


# ============================================================================
# ON-CHAIN ANALYTICS
# ============================================================================

def fetch_chainalysis_flows(regions: List[str] = None) -> pd.DataFrame:
    """
    Fetch on-chain crypto flows by region
    
    Chainalysis provides geographic attribution of blockchain transactions
    
    API: https://www.chainalysis.com/
    Requires paid subscription
    """
    # Placeholder - would need Chainalysis API key
    
    if regions is None:
        regions = ['North America', 'Europe', 'Asia', 'Latin America', 'Africa']
    
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    data = []
    for region in regions:
        for date in dates:
            data.append({
                'date': date,
                'region': region,
                'inflow_btc': 1000 + (hash(f"{region}{date}") % 500),
                'outflow_btc': 950 + (hash(f"{region}{date}") % 500),
                'net_flow_btc': 50
            })
    
    return pd.DataFrame(data)


def fetch_mixer_usage() -> pd.DataFrame:
    """
    Track privacy tool usage (mixers, CoinJoin, Tornado Cash)
    
    Increased usage = increased demand for transaction privacy
    Often correlates with regulatory pressure or capital controls
    """
    # Would integrate with blockchain analytics platforms
    # Example: Dune Analytics queries for mixer volumes
    
    dates = pd.date_range(end=datetime.now(), periods=180, freq='D')
    
    return pd.DataFrame({
        'date': dates,
        'tornado_cash_volume_eth': [100 + (i % 50)*10 for i in range(len(dates))],
        'wasabi_volume_btc': [50 + (i % 30)*5 for i in range(len(dates))],
        'coinjoin_transactions': [200 + (i % 100)*20 for i in range(len(dates))]
    })


# ============================================================================
# ECONOMIC INDICATORS
# ============================================================================

def fetch_black_market_rates(countries: List[str] = None) -> pd.DataFrame:
    """
    Fetch black market exchange rates
    
    Source: DolarToday, Trading Economics, local market data
    
    Large divergence from official rate = severe capital controls
    """
    # Example for Venezuela, Argentina, Lebanon, etc.
    
    if countries is None:
        countries = ['Venezuela', 'Argentina', 'Lebanon']
    
    # Would fetch from Trading Economics API or DolarToday
    
    return pd.DataFrame({
        'country': countries,
        'date': datetime.now(),
        'official_rate': [10, 350, 15000],
        'black_market_rate': [35, 1000, 85000],
        'premium_pct': [250, 186, 467]
    })


def fetch_inflation_data(countries: List[str] = None) -> pd.DataFrame:
    """
    Fetch inflation rates by country
    
    API: World Bank, IMF, Trading Economics
    
    High inflation often correlates with crypto adoption
    """
    # Would use World Bank API or similar
    
    if countries is None:
        countries = ['Venezuela', 'Argentina', 'Turkey', 'Lebanon', 'Nigeria']
    
    return pd.DataFrame({
        'country': countries,
        'inflation_rate_annual': [150.0, 120.0, 65.0, 200.0, 25.0],
        'inflation_rank': [2, 3, 8, 1, 20],
        'last_updated': datetime.now()
    })


# ============================================================================
# STABLECOIN ANALYTICS
# ============================================================================

def fetch_defillama_stablecoins() -> pd.DataFrame:
    """
    Fetch real stablecoin supply data from DeFiLlama
    
    API: https://defillama.com/docs/api
    Free and comprehensive
    """
    try:
        url = "https://stablecoins.llama.fi/stablecoins"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract stablecoin data
            stablecoins = []
            for coin in data.get('peggedAssets', []):
                stablecoins.append({
                    'name': coin.get('name'),
                    'symbol': coin.get('symbol'),
                    'circulating': coin.get('circulating', {}).get('peggedUSD', 0),
                    'chains': len(coin.get('chainCirculating', {}))
                })
            
            return pd.DataFrame(stablecoins)
    
    except Exception as e:
        print(f"Error fetching DeFiLlama data: {e}")
    
    return pd.DataFrame()


def fetch_stablecoin_flows_by_chain() -> pd.DataFrame:
    """
    Track stablecoin flows between chains
    
    Bridge activity can indicate:
    - Capital moving to lower-regulation chains
    - Flight from specific ecosystems
    - Geographic routing patterns
    """
    # Would integrate with bridge analytics (Dune, Nansen)
    
    chains = ['Ethereum', 'BSC', 'Polygon', 'Arbitrum', 'Optimism', 'Tron']
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    data = []
    for chain in chains:
        for date in dates:
            data.append({
                'date': date,
                'chain': chain,
                'total_stablecoins_usd': 1e9 + (hash(f"{chain}{date}") % 1e8),
                'daily_transfer_volume': 100e6 + (hash(f"{chain}{date}") % 50e6)
            })
    
    return pd.DataFrame(data)


# ============================================================================
# REGULATORY TRACKING
# ============================================================================

def fetch_regulatory_actions() -> pd.DataFrame:
    """
    Track regulatory enforcement actions
    
    Sources:
    - SEC litigation releases
    - CFTC enforcement actions  
    - FinCEN advisories
    - International regulatory bodies
    """
    # Would scrape from regulatory websites or use specialized APIs
    
    actions = [
        {
            'date': '2023-06-05',
            'agency': 'SEC',
            'target': 'Binance',
            'action_type': 'Lawsuit',
            'severity': 8
        },
        {
            'date': '2023-06-06',
            'agency': 'SEC',
            'target': 'Coinbase',
            'action_type': 'Lawsuit',
            'severity': 7
        },
        # More would be added from automated scraping
    ]
    
    return pd.DataFrame(actions)


# ============================================================================
# CORRUPTION INDICES
# ============================================================================

def fetch_corruption_perception_index() -> pd.DataFrame:
    """
    Transparency International Corruption Perceptions Index
    
    Annual ranking of countries by perceived corruption
    Could correlate with crypto adoption rates
    """
    # Data available at: https://www.transparency.org/en/cpi
    
    # Example data (2023)
    countries = [
        ('Denmark', 90, 1),
        ('Finland', 87, 2),
        ('New Zealand', 87, 2),
        ('USA', 69, 24),
        ('China', 42, 76),
        ('Russia', 26, 141),
        ('Venezuela', 13, 177),
    ]
    
    return pd.DataFrame(countries, columns=['country', 'cpi_score', 'rank'])


def fetch_capital_control_index() -> pd.DataFrame:
    """
    Chinn-Ito Index of capital account openness
    
    Academic standard for measuring capital controls
    Higher score = more open capital account
    """
    # Available at: http://web.pdx.edu/~ito/Chinn-Ito_website.htm
    
    # Placeholder structure
    return pd.DataFrame({
        'country': ['USA', 'UK', 'China', 'India', 'Argentina'],
        'kaopen_score': [2.44, 2.44, -1.17, -1.17, -0.13],
        'year': 2023
    })


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    """
    Example: How to integrate these into your Streamlit app
    """
    
    # 1. Add to your imports
    # from data_collection_extensions import fetch_defillama_stablecoins
    
    # 2. Use in your Streamlit app:
    # st.markdown("### Real Stablecoin Data")
    # stablecoin_data = fetch_defillama_stablecoins()
    # st.dataframe(stablecoin_data)
    
    # 3. Cache for performance:
    # @st.cache_data(ttl=3600)
    # def get_cached_stablecoins():
    #     return fetch_defillama_stablecoins()
    
    print("Data collection extensions loaded successfully")
    print("\nExample: Fetching DeFiLlama stablecoin data...")
    
    df = fetch_defillama_stablecoins()
    if not df.empty:
        print(f"\nFound {len(df)} stablecoins")
        print(df.head())
    
    print("\nTo use these functions:")
    print("1. Copy this file to your project directory")
    print("2. Import the functions you need")
    print("3. Add to your Streamlit app with @st.cache_data decorator")
