"""
Configuration File for Crypto Corruption Index
==============================================

Customize the application behavior, data sources, and analysis parameters here.
"""

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_CONFIG = {
    'title': 'Crypto Corruption Index',
    'page_icon': '📊',
    'layout': 'wide',
    'theme': {
        'primary_color': '#1f77b4',
        'background_color': '#ffffff',
        'secondary_background_color': '#f0f2f6'
    }
}

# ============================================================================
# DATA SOURCES
# ============================================================================

# Crypto Market Data
CRYPTO_ASSETS = {
    'bitcoin': {
        'coingecko_id': 'bitcoin',
        'symbol': 'BTC',
        'category': 'benchmark',
        'leverage_recommended': 1.0
    },
    'ethereum': {
        'coingecko_id': 'ethereum',
        'symbol': 'ETH',
        'category': 'platform',
        'leverage_recommended': 1.0
    },
    'tether': {
        'coingecko_id': 'tether',
        'symbol': 'USDT',
        'category': 'stablecoin',
        'leverage_recommended': 2.0
    },
    'usd-coin': {
        'coingecko_id': 'usd-coin',
        'symbol': 'USDC',
        'category': 'stablecoin',
        'leverage_recommended': 2.0
    },
    'monero': {
        'coingecko_id': 'monero',
        'symbol': 'XMR',
        'category': 'privacy',
        'leverage_recommended': 1.0
    },
    'zcash': {
        'coingecko_id': 'zcash',
        'symbol': 'ZEC',
        'category': 'privacy',
        'leverage_recommended': 1.0
    }
}

# API Configuration
API_CONFIG = {
    'coingecko': {
        'base_url': 'https://api.coingecko.com/api/v3',
        'rate_limit_per_minute': 10,
        'cache_ttl_seconds': 3600
    },
    'defillama': {
        'base_url': 'https://stablecoins.llama.fi',
        'cache_ttl_seconds': 7200
    }
}

# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

# Corruption Index Calculation
CORRUPTION_INDEX_WEIGHTS = {
    'volatility': 0.30,      # Weight for price volatility component
    'volume_surge': 0.30,    # Weight for volume z-score component
    'event_intensity': 0.40  # Weight for policy event component
}

CORRUPTION_INDEX_PARAMS = {
    'volatility_window_days': 30,   # Rolling window for volatility calculation
    'volume_window_days': 90,       # Window for volume z-score baseline
    'event_window_days': 7,         # Days to attribute event impact
    'scale_min': 0,                 # Minimum index value
    'scale_max': 100                # Maximum index value
}

# Event Study Parameters
EVENT_STUDY_CONFIG = {
    'window_before_days': 30,       # Days before event to include
    'window_after_days': 30,        # Days after event to include
    'crisis_window_days': 7,        # Window for measuring crisis response
    'significance_threshold': 0.05  # P-value threshold for statistical tests
}

# ============================================================================
# PORTFOLIO OPTIMIZATION
# ============================================================================

# Expected Returns (annual %)
EXPECTED_RETURNS = {
    'Bitcoin': {
        'base_case': 0.25,          # 25% in normal conditions
        'crisis_alpha': 2.0,        # 2x multiple during crises
        'max_drawdown': -0.60       # -60% worst case
    },
    'Ethereum': {
        'base_case': 0.30,
        'crisis_alpha': 2.5,
        'max_drawdown': -0.65
    },
    'Stablecoins': {
        'base_case': 0.08,          # 8% yield farming returns
        'crisis_alpha': 1.2,        # 1.2x during capital flight
        'max_drawdown': -0.15       # -15% (depeg risk)
    },
    'Privacy': {
        'base_case': 0.20,
        'crisis_alpha': 1.5,
        'max_drawdown': -0.55
    }
}

# Leverage Limits
LEVERAGE_CONFIG = {
    'stablecoin_max': 3.0,
    'stablecoin_recommended': 2.0,
    'volatile_max': 2.0,
    'volatile_recommended': 1.0
}

# Default Portfolio Allocation (%)
DEFAULT_PORTFOLIO = {
    'bitcoin': 30,
    'ethereum': 20,
    'stablecoins': 40,
    'privacy': 10
}

# ============================================================================
# GEOGRAPHIC FOCUS
# ============================================================================

# Countries with high policy friction
HIGH_FRICTION_COUNTRIES = [
    'Russia', 'China', 'Venezuela', 'Argentina', 'Lebanon',
    'Turkey', 'Nigeria', 'Iran', 'Cuba', 'North Korea'
]

# Regions for analysis
REGIONS = {
    'North America': ['USA', 'Canada', 'Mexico'],
    'South America': ['Brazil', 'Argentina', 'Chile', 'Venezuela', 'Colombia'],
    'Europe': ['UK', 'Germany', 'France', 'Russia', 'Ukraine'],
    'Asia': ['China', 'Japan', 'South Korea', 'India', 'Singapore'],
    'Middle East': ['UAE', 'Saudi Arabia', 'Iran', 'Lebanon', 'Turkey'],
    'Africa': ['Nigeria', 'South Africa', 'Kenya', 'Egypt']
}

# ============================================================================
# EVENT CLASSIFICATION
# ============================================================================

# Event Types and Severity Ranges
EVENT_TYPES = {
    'Sanctions': {
        'description': 'International sanctions, SWIFT removal, asset freezes',
        'typical_severity': (7, 10),
        'crypto_response': 'high'
    },
    'Capital Controls': {
        'description': 'Forex restrictions, withdrawal limits, currency devaluation',
        'typical_severity': (5, 9),
        'crypto_response': 'very_high'
    },
    'Banking': {
        'description': 'Bank runs, deposit restrictions, banking sector stress',
        'typical_severity': (6, 9),
        'crypto_response': 'high'
    },
    'Regulatory': {
        'description': 'Crypto bans, KYC enforcement, exchange crackdowns',
        'typical_severity': (4, 8),
        'crypto_response': 'medium'
    },
    'Market': {
        'description': 'Exchange collapses, depegs, protocol failures',
        'typical_severity': (5, 9),
        'crypto_response': 'variable'
    }
}

# Severity Score Guidelines
SEVERITY_GUIDELINES = {
    1: 'Minor: Local regulatory clarification, small exchange licensing',
    2: 'Low: Limited KYC requirements, minor tax reporting changes',
    3: 'Moderate: Exchange restrictions in small markets',
    4: 'Noticeable: Significant but localized regulatory action',
    5: 'Medium: Major exchange shut down, mid-size country restrictions',
    6: 'Significant: Large country regulatory crackdown',
    7: 'High: Major banking crisis, targeted sanctions',
    8: 'Severe: Systemic banking failure, broad sanctions',
    9: 'Critical: SWIFT removal, nationwide crypto ban in major economy',
    10: 'Extreme: Multi-country coordinated action, global systemic event'
}

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

CHART_CONFIG = {
    'color_scheme': {
        'bitcoin': '#f7931a',
        'ethereum': '#627eea',
        'stablecoin': '#26a17b',
        'privacy': '#4c4c4c',
        'index': '#d62728',
        'event_marker': '#808080'
    },
    'default_height': 500,
    'default_width': None,  # Auto-width
    'theme': 'plotly'
}

# ============================================================================
# DATA QUALITY & VALIDATION
# ============================================================================

DATA_QUALITY = {
    'min_data_points': 30,          # Minimum days of data required
    'max_missing_pct': 0.10,        # Maximum 10% missing data allowed
    'outlier_threshold_std': 5,     # Z-score threshold for outlier detection
    'price_change_limit_pct': 100   # Flag if daily price change > 100%
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    'enable_web_search': True,          # Allow web searches for event discovery
    'enable_user_events': True,         # Allow users to add events
    'enable_portfolio_export': True,    # Export portfolio to CSV
    'enable_backtesting': False,        # Backtesting module (future)
    'enable_ml_predictions': False,     # ML predictions (future)
    'enable_alerts': False,             # Real-time alerts (future)
}

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

ADVANCED = {
    'statistical_methods': {
        'correlation_method': 'pearson',  # 'pearson', 'spearman', 'kendall'
        'return_calculation': 'log',       # 'log' or 'simple'
        'volatility_method': 'std'         # 'std', 'parkinson', 'garman_klass'
    },
    'risk_metrics': {
        'confidence_level': 0.95,          # For VaR calculations
        'sharpe_risk_free_rate': 0.03      # 3% risk-free rate assumption
    }
}

# ============================================================================
# EXAMPLE CUSTOMIZATION
# ============================================================================

"""
To customize the application:

1. Modify CORRUPTION_INDEX_WEIGHTS to change how the index is calculated
2. Add new assets to CRYPTO_ASSETS 
3. Adjust EVENT_STUDY_CONFIG to change analysis windows
4. Update EXPECTED_RETURNS based on your research
5. Modify CHART_CONFIG colors to match your brand

Then restart the Streamlit app to apply changes.
"""

# ============================================================================
# EXPORT FOR USE IN MAIN APP
# ============================================================================

def get_config(section: str = None):
    """
    Get configuration dictionary
    
    Args:
        section: Optional section name to retrieve
                ('app', 'crypto', 'api', 'corruption_index', etc.)
    
    Returns:
        Dictionary of configuration values
    """
    config_map = {
        'app': APP_CONFIG,
        'crypto': CRYPTO_ASSETS,
        'api': API_CONFIG,
        'corruption_index': {
            'weights': CORRUPTION_INDEX_WEIGHTS,
            'params': CORRUPTION_INDEX_PARAMS
        },
        'events': {
            'types': EVENT_TYPES,
            'severity': SEVERITY_GUIDELINES,
            'study_config': EVENT_STUDY_CONFIG
        },
        'portfolio': {
            'returns': EXPECTED_RETURNS,
            'leverage': LEVERAGE_CONFIG,
            'default': DEFAULT_PORTFOLIO
        },
        'geography': {
            'high_friction': HIGH_FRICTION_COUNTRIES,
            'regions': REGIONS
        },
        'visualization': CHART_CONFIG,
        'data_quality': DATA_QUALITY,
        'features': FEATURES,
        'advanced': ADVANCED
    }
    
    if section:
        return config_map.get(section, {})
    
    return config_map


if __name__ == "__main__":
    """Test configuration loading"""
    print("Configuration loaded successfully")
    print(f"\nTracking {len(CRYPTO_ASSETS)} crypto assets")
    print(f"Event types: {list(EVENT_TYPES.keys())}")
    print(f"High friction countries: {len(HIGH_FRICTION_COUNTRIES)}")
    print(f"\nCorruption index weights:")
    for component, weight in CORRUPTION_INDEX_WEIGHTS.items():
        print(f"  {component}: {weight*100}%")
