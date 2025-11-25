import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Tuple
import json

# Page config
st.set_page_config(
    page_title="Crypto Corruption Index",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio(
    "Select Analysis",
    ["Overview", "Market Data", "Policy Events", "Correlation Analysis", "Portfolio Builder", "Data Sources"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This tool analyzes cryptocurrency as an index for policy friction and corruption premiums.

**Thesis**: Crypto prices/volumes reflect aggregated willingness-to-pay for circumventing formal institutional systems.
""")

# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def fetch_crypto_prices(symbols: List[str] = ['bitcoin', 'ethereum', 'tether', 'monero'], 
                        days: int = 365) -> pd.DataFrame:
    """Fetch historical crypto prices from CoinGecko API"""
    all_data = []
    
    for symbol in symbols:
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                df['symbol'] = symbol
                df['volume'] = [v[1] for v in data.get('total_volumes', [])]
                all_data.append(df[['date', 'symbol', 'price', 'volume']])
        except Exception as e:
            st.warning(f"Could not fetch data for {symbol}: {str(e)}")
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def fetch_stablecoin_supply() -> pd.DataFrame:
    """Fetch stablecoin supply metrics (simplified - would need proper API)"""
    # This is a placeholder - in production would use DeFiLlama or similar
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    
    # Simulated data for demonstration
    np.random.seed(42)
    base_supply = 100e9  # 100 billion base
    trend = np.linspace(0, 50e9, len(dates))
    noise = np.random.normal(0, 5e9, len(dates))
    
    return pd.DataFrame({
        'date': dates,
        'total_supply': base_supply + trend + noise,
        'usdt_supply': (base_supply + trend + noise) * 0.6,
        'usdc_supply': (base_supply + trend + noise) * 0.3,
        'dai_supply': (base_supply + trend + noise) * 0.1
    })

def get_policy_events() -> pd.DataFrame:
    """Database of known policy friction events"""
    events = [
        {
            'date': '2022-02-24',
            'country': 'Russia',
            'event_type': 'Sanctions',
            'description': 'Russia-Ukraine war sanctions begin',
            'severity': 9
        },
        {
            'date': '2022-03-09',
            'country': 'Russia',
            'event_type': 'Banking',
            'description': 'Russia removed from SWIFT',
            'severity': 10
        },
        {
            'date': '2023-02-28',
            'country': 'Nigeria',
            'event_type': 'Capital Controls',
            'description': 'Nigeria naira devaluation and cash withdrawal limits',
            'severity': 7
        },
        {
            'date': '2022-06-15',
            'country': 'Lebanon',
            'event_type': 'Banking',
            'description': 'Lebanon banking crisis deepens, deposit withdrawals restricted',
            'severity': 8
        },
        {
            'date': '2023-03-10',
            'country': 'USA',
            'event_type': 'Banking',
            'description': 'Silicon Valley Bank collapse',
            'severity': 8
        },
        {
            'date': '2022-11-08',
            'country': 'Global',
            'event_type': 'Regulatory',
            'description': 'FTX collapse triggers regulatory scrutiny',
            'severity': 7
        },
        {
            'date': '2023-06-05',
            'country': 'USA',
            'event_type': 'Regulatory',
            'description': 'SEC sues Binance and Coinbase',
            'severity': 6
        },
        {
            'date': '2021-09-24',
            'country': 'China',
            'event_type': 'Regulatory',
            'description': 'China declares all crypto transactions illegal',
            'severity': 9
        },
        {
            'date': '2023-08-09',
            'country': 'Argentina',
            'event_type': 'Capital Controls',
            'description': 'Peso devaluation accelerates, capital flight',
            'severity': 8
        },
        {
            'date': '2022-05-09',
            'country': 'Global',
            'event_type': 'Market',
            'description': 'Terra/LUNA collapse',
            'severity': 9
        }
    ]
    
    df = pd.DataFrame(events)
    df['date'] = pd.to_datetime(df['date'])
    return df

def calculate_corruption_index(crypto_data: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """Calculate a composite corruption/friction index"""
    # Aggregate crypto metrics by date
    daily_metrics = crypto_data.groupby('date').agg({
        'price': 'mean',
        'volume': 'sum'
    }).reset_index()
    
    # Calculate volatility (30-day rolling std)
    daily_metrics['volatility'] = daily_metrics['price'].rolling(30).std()
    
    # Calculate volume surges (z-score)
    daily_metrics['volume_zscore'] = (
        daily_metrics['volume'] - daily_metrics['volume'].rolling(90).mean()
    ) / daily_metrics['volume'].rolling(90).std()
    
    # Add event intensity (sum of severity in 7-day window)
    daily_metrics['event_intensity'] = 0
    for _, event in events.iterrows():
        mask = (daily_metrics['date'] >= event['date']) & \
               (daily_metrics['date'] < event['date'] + timedelta(days=7))
        daily_metrics.loc[mask, 'event_intensity'] += event['severity']
    
    # Composite corruption index (normalized 0-100)
    daily_metrics['corruption_index'] = (
        daily_metrics['volatility'].fillna(0) / daily_metrics['volatility'].max() * 30 +
        daily_metrics['volume_zscore'].clip(-3, 3).fillna(0) / 6 * 30 +
        daily_metrics['event_intensity'] / daily_metrics['event_intensity'].max() * 40
    ).fillna(0)
    
    return daily_metrics

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

if page == "Overview":
    st.markdown('<p class="main-header">📊 Crypto Corruption Index</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Theory
    
    Cryptocurrency markets can be analyzed as a **revealed preference index for institutional friction costs**. 
    The "corruption premium" measures what economic actors will pay to circumvent formal systems, including:
    
    - 🏛️ **Regulatory Arbitrage** - Routing around inefficient rules
    - 🌐 **Sanctions Evasion** - Geopolitically-driven capital flows
    - 💰 **Capital Flight** - Protection from unstable governments
    - 🔒 **Privacy Premium** - Demand for financial opacity
    - ⚠️ **Institutional Distrust** - Flight from traditional finance
    
    ### Expected Yield Characteristics
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Base Case Annual Yield", "15-30%", help="Structural demand from persistent policy friction")
    
    with col2:
        st.metric("Crisis Alpha Potential", "2-5x", help="Spikes during capital controls, banking failures, sanctions")
    
    with col3:
        st.metric("Maximum Drawdown", "-50-70%", help="Risk during coordinated regulatory crackdowns")
    
    st.markdown("---")
    
    # Load and display recent index
    with st.spinner("Loading market data..."):
        crypto_data = fetch_crypto_prices(days=365)
        events = get_policy_events()
        
        if not crypto_data.empty:
            corruption_index = calculate_corruption_index(crypto_data, events)
            
            # Display current index value
            latest = corruption_index.iloc[-1]
            
            st.markdown("### Current Corruption Index")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Index Value",
                    f"{latest['corruption_index']:.1f}",
                    delta=f"{latest['corruption_index'] - corruption_index.iloc[-30]['corruption_index']:.1f}",
                    help="Composite measure of policy friction (0-100 scale)"
                )
            
            with col2:
                st.metric(
                    "Volume Z-Score",
                    f"{latest['volume_zscore']:.2f}",
                    help="Standard deviations above mean volume"
                )
            
            with col3:
                st.metric(
                    "Volatility",
                    f"{latest['volatility']:.0f}",
                    help="30-day price volatility"
                )
            
            with col4:
                st.metric(
                    "Event Intensity",
                    f"{latest['event_intensity']:.0f}",
                    help="Recent policy friction events (severity sum)"
                )
            
            # Plot the index
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=corruption_index['date'],
                y=corruption_index['corruption_index'],
                mode='lines',
                name='Corruption Index',
                line=dict(color='#d62728', width=2),
                fill='tozeroy',
                fillcolor='rgba(214, 39, 40, 0.1)'
            ))
            
            # Add event markers
            for _, event in events.iterrows():
                fig.add_vline(
                    x=event['date'],
                    line_dash="dash",
                    line_color="gray",
                    annotation_text=event['country'],
                    annotation_position="top"
                )
            
            fig.update_layout(
                title="Crypto Corruption Index Over Time",
                xaxis_title="Date",
                yaxis_title="Index Value (0-100)",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Interpretation**: Spikes in the index indicate periods of heightened policy friction where 
            cryptocurrency demand increases due to capital controls, sanctions, banking crises, or regulatory uncertainty.
            """)

# ============================================================================
# PAGE: MARKET DATA
# ============================================================================

elif page == "Market Data":
    st.markdown('<p class="main-header">💹 Crypto Market Data</p>', unsafe_allow_html=True)
    
    # Asset selection
    st.sidebar.markdown("### Asset Selection")
    selected_assets = st.sidebar.multiselect(
        "Choose cryptocurrencies",
        ['bitcoin', 'ethereum', 'tether', 'usd-coin', 'monero', 'zcash'],
        default=['bitcoin', 'ethereum', 'tether', 'monero']
    )
    
    days_back = st.sidebar.slider("Days of history", 30, 730, 365)
    
    if selected_assets:
        with st.spinner("Fetching market data..."):
            crypto_data = fetch_crypto_prices(selected_assets, days=days_back)
            
            if not crypto_data.empty:
                # Price comparison
                st.markdown("### Price Trends")
                
                fig = px.line(
                    crypto_data,
                    x='date',
                    y='price',
                    color='symbol',
                    title='Asset Prices Over Time (USD)',
                    log_y=True
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Volume analysis
                st.markdown("### Trading Volume")
                
                fig = px.bar(
                    crypto_data,
                    x='date',
                    y='volume',
                    color='symbol',
                    title='Trading Volume by Asset'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Correlation matrix
                st.markdown("### Asset Correlations")
                
                pivot_prices = crypto_data.pivot(index='date', columns='symbol', values='price')
                correlation = pivot_prices.corr()
                
                fig = px.imshow(
                    correlation,
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    aspect='auto',
                    title='Price Correlation Matrix'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Stablecoin supply
                st.markdown("### Stablecoin Supply (Proxy for Capital Flight)")
                
                stablecoin_data = fetch_stablecoin_supply()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=stablecoin_data['date'],
                    y=stablecoin_data['total_supply'] / 1e9,
                    mode='lines',
                    name='Total Supply',
                    line=dict(width=3)
                ))
                
                fig.update_layout(
                    title='Stablecoin Supply Growth',
                    xaxis_title='Date',
                    yaxis_title='Supply (Billions USD)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("📊 Stablecoin supply growth often correlates with capital flight from traditional banking systems.")

# ============================================================================
# PAGE: POLICY EVENTS
# ============================================================================

elif page == "Policy Events":
    st.markdown('<p class="main-header">⚖️ Policy Friction Events</p>', unsafe_allow_html=True)
    
    events = get_policy_events()
    
    st.markdown("""
    This database tracks major policy friction events that create demand for cryptocurrency as a circumvention mechanism.
    """)
    
    # Event type filter
    event_types = ['All'] + sorted(events['event_type'].unique().tolist())
    selected_type = st.selectbox("Filter by event type", event_types)
    
    if selected_type != 'All':
        filtered_events = events[events['event_type'] == selected_type]
    else:
        filtered_events = events
    
    # Display events timeline
    fig = px.scatter(
        filtered_events,
        x='date',
        y='severity',
        size='severity',
        color='event_type',
        hover_data=['country', 'description'],
        title='Policy Friction Events Timeline'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Events by country
    st.markdown("### Events by Geography")
    country_counts = filtered_events['country'].value_counts()
    
    fig = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        labels={'x': 'Country', 'y': 'Number of Events'},
        title='Policy Friction Events by Country'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed event table
    st.markdown("### Event Details")
    
    display_df = filtered_events.sort_values('date', ascending=False).copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        display_df,
        column_config={
            'severity': st.column_config.ProgressColumn(
                'Severity',
                min_value=0,
                max_value=10
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Add new event form
    with st.expander("➕ Add New Policy Event"):
        with st.form("new_event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_date = st.date_input("Event Date")
                new_country = st.text_input("Country")
                new_type = st.selectbox("Event Type", 
                    ['Sanctions', 'Capital Controls', 'Banking', 'Regulatory', 'Market'])
            
            with col2:
                new_severity = st.slider("Severity", 1, 10, 5)
                new_description = st.text_area("Description")
            
            submitted = st.form_submit_button("Add Event")
            
            if submitted:
                st.success(f"Event added: {new_country} - {new_description[:50]}...")
                st.info("Note: In production, this would save to a database")

# ============================================================================
# PAGE: CORRELATION ANALYSIS
# ============================================================================

elif page == "Correlation Analysis":
    st.markdown('<p class="main-header">📈 Event-Driven Correlation Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    This analysis tests whether crypto prices/volumes spike following policy friction events.
    
    **Hypothesis**: Crypto premiums should increase within 1-7 days of capital controls, sanctions, 
    banking crises, or major regulatory actions.
    """)
    
    with st.spinner("Analyzing correlations..."):
        crypto_data = fetch_crypto_prices(days=730)
        events = get_policy_events()
        
        if not crypto_data.empty:
            # Event study analysis
            st.markdown("### Event Study: Price Response")
            
            selected_event = st.selectbox(
                "Select event to analyze",
                events.sort_values('date', ascending=False).apply(
                    lambda x: f"{x['date'].strftime('%Y-%m-%d')} - {x['country']} - {x['description'][:50]}",
                    axis=1
                )
            )
            
            event_idx = int(selected_event.split(' - ')[0])
            event = events[events['date'] == event_idx].iloc[0] if len(events[events['date'] == event_idx]) > 0 else events.iloc[0]
            
            # Get price data around event
            event_date = events.iloc[0]['date']  # Simplified for demo
            window_start = event_date - timedelta(days=30)
            window_end = event_date + timedelta(days=30)
            
            event_window = crypto_data[
                (crypto_data['date'] >= window_start) & 
                (crypto_data['date'] <= window_end)
            ].copy()
            
            event_window['days_from_event'] = (event_window['date'] - event_date).dt.days
            
            # Plot price movements around event
            fig = px.line(
                event_window,
                x='days_from_event',
                y='price',
                color='symbol',
                title=f'Price Movement Around Event (Day 0 = {event_date.strftime("%Y-%m-%d")})'
            )
            
            fig.add_vline(x=0, line_dash="dash", line_color="red", 
                         annotation_text="Event Date")
            
            fig.update_layout(
                xaxis_title='Days from Event',
                yaxis_title='Price (USD)',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate returns
            st.markdown("### Cumulative Returns Analysis")
            
            returns_data = []
            for symbol in event_window['symbol'].unique():
                symbol_data = event_window[event_window['symbol'] == symbol].copy()
                symbol_data = symbol_data.sort_values('days_from_event')
                
                if len(symbol_data) > 0:
                    base_price = symbol_data[symbol_data['days_from_event'] == 0]['price'].values
                    if len(base_price) > 0:
                        symbol_data['cumulative_return'] = (
                            (symbol_data['price'] / base_price[0] - 1) * 100
                        )
                        returns_data.append(symbol_data)
            
            if returns_data:
                returns_df = pd.concat(returns_data)
                
                fig = px.line(
                    returns_df,
                    x='days_from_event',
                    y='cumulative_return',
                    color='symbol',
                    title='Cumulative Returns from Event Date (%)'
                )
                
                fig.add_vline(x=0, line_dash="dash", line_color="red")
                fig.add_hline(y=0, line_dash="dot", line_color="gray")
                
                fig.update_layout(
                    xaxis_title='Days from Event',
                    yaxis_title='Return (%)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Statistical summary
            st.markdown("### Statistical Summary")
            
            col1, col2, col3 = st.columns(3)
            
            # Calculate average returns at different windows
            for symbol in event_window['symbol'].unique():
                symbol_data = event_window[event_window['symbol'] == symbol]
                
                pre_event = symbol_data[symbol_data['days_from_event'] < 0]['price'].mean()
                post_event_7d = symbol_data[
                    (symbol_data['days_from_event'] >= 0) & 
                    (symbol_data['days_from_event'] <= 7)
                ]['price'].mean()
                
                if pre_event > 0:
                    change_pct = ((post_event_7d / pre_event) - 1) * 100
                    
                    with col1:
                        st.metric(
                            f"{symbol.title()} 7-day return",
                            f"{change_pct:+.2f}%"
                        )
            
            st.info("""
            **Interpretation**: Positive returns in the 7-day window following policy events 
            suggest that crypto acts as a hedge or escape mechanism during institutional friction.
            """)

# ============================================================================
# PAGE: PORTFOLIO BUILDER
# ============================================================================

elif page == "Portfolio Builder":
    st.markdown('<p class="main-header">💼 Corruption-Weighted Portfolio</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Build a portfolio optimized for capturing policy friction premiums across different crypto instruments.
    """)
    
    # Portfolio allocation inputs
    st.markdown("### Asset Allocation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Core Holdings")
        btc_weight = st.slider("Bitcoin (%)", 0, 100, 30)
        eth_weight = st.slider("Ethereum (%)", 0, 100, 20)
        stablecoin_weight = st.slider("Stablecoins (%)", 0, 100, 40)
    
    with col2:
        st.markdown("#### Specialized")
        privacy_weight = st.slider("Privacy Coins (%)", 0, 100, 10)
        
        total_weight = btc_weight + eth_weight + stablecoin_weight + privacy_weight
        st.metric("Total Allocation", f"{total_weight}%")
        
        if total_weight != 100:
            st.warning(f"⚠️ Allocation must equal 100% (currently {total_weight}%)")
    
    # Leverage settings
    st.markdown("### Leverage Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stablecoin_leverage = st.slider("Stablecoin Leverage", 1.0, 3.0, 2.0, 0.1)
        other_leverage = st.slider("Other Assets Leverage", 1.0, 2.0, 1.0, 0.1)
    
    with col2:
        st.info("""
        **Recommendation**: Use 2-3x leverage on stablecoins (most predictable), 
        1x on other assets to manage volatility.
        """)
    
    # Calculate portfolio metrics
    if total_weight == 100:
        st.markdown("### Expected Portfolio Performance")
        
        # Simplified expected returns (would use historical data in production)
        expected_returns = {
            'Bitcoin': {'base': 0.25, 'crisis': 2.0, 'drawdown': -0.60},
            'Ethereum': {'base': 0.30, 'crisis': 2.5, 'drawdown': -0.65},
            'Stablecoins': {'base': 0.08, 'crisis': 1.2, 'drawdown': -0.15},
            'Privacy': {'base': 0.20, 'crisis': 1.5, 'drawdown': -0.55}
        }
        
        portfolio_base = (
            btc_weight/100 * expected_returns['Bitcoin']['base'] * other_leverage +
            eth_weight/100 * expected_returns['Ethereum']['base'] * other_leverage +
            stablecoin_weight/100 * expected_returns['Stablecoins']['base'] * stablecoin_leverage +
            privacy_weight/100 * expected_returns['Privacy']['base'] * other_leverage
        )
        
        portfolio_crisis = (
            btc_weight/100 * expected_returns['Bitcoin']['crisis'] * other_leverage +
            eth_weight/100 * expected_returns['Ethereum']['crisis'] * other_leverage +
            stablecoin_weight/100 * expected_returns['Stablecoins']['crisis'] * stablecoin_leverage +
            privacy_weight/100 * expected_returns['Privacy']['crisis'] * other_leverage
        )
        
        portfolio_drawdown = (
            btc_weight/100 * expected_returns['Bitcoin']['drawdown'] * other_leverage +
            eth_weight/100 * expected_returns['Ethereum']['drawdown'] * other_leverage +
            stablecoin_weight/100 * expected_returns['Stablecoins']['drawdown'] * stablecoin_leverage +
            privacy_weight/100 * expected_returns['Privacy']['drawdown'] * other_leverage
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Base Case Annual Return",
                f"{portfolio_base*100:.1f}%",
                help="Expected return in normal market conditions"
            )
        
        with col2:
            st.metric(
                "Crisis Alpha Multiple",
                f"{portfolio_crisis:.1f}x",
                help="Expected multiple during policy friction events"
            )
        
        with col3:
            st.metric(
                "Maximum Drawdown",
                f"{portfolio_drawdown*100:.1f}%",
                delta=f"{portfolio_drawdown*100:.1f}%",
                delta_color="inverse",
                help="Worst-case loss scenario"
            )
        
        # Allocation visualization
        allocation_df = pd.DataFrame({
            'Asset': ['Bitcoin', 'Ethereum', 'Stablecoins', 'Privacy Coins'],
            'Weight': [btc_weight, eth_weight, stablecoin_weight, privacy_weight],
            'Leverage': [other_leverage, other_leverage, stablecoin_leverage, other_leverage]
        })
        
        allocation_df['Effective Exposure'] = allocation_df['Weight'] * allocation_df['Leverage']
        
        fig = px.pie(
            allocation_df,
            values='Effective Exposure',
            names='Asset',
            title='Leveraged Portfolio Exposure'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk warning
        st.warning("""
        ⚠️ **Risk Disclaimer**: This portfolio strategy involves significant risk. 
        Leverage amplifies both gains and losses. Crypto markets are highly volatile and 
        regulatory changes can occur rapidly. Past performance does not guarantee future results.
        """)

# ============================================================================
# PAGE: DATA SOURCES
# ============================================================================

elif page == "Data Sources":
    st.markdown('<p class="main-header">🔗 Data Sources & Methodology</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Current Data Sources
    
    This application currently uses the following data sources:
    """)
    
    sources = [
        {
            'name': 'CoinGecko API',
            'type': 'Crypto Market Data',
            'description': 'Historical prices, volumes, and market caps for major cryptocurrencies',
            'status': '✅ Active',
            'url': 'https://www.coingecko.com/en/api'
        },
        {
            'name': 'Manual Event Database',
            'type': 'Policy Friction Events',
            'description': 'Curated database of sanctions, capital controls, banking crises, and regulatory actions',
            'status': '⚠️ Manual Entry',
            'url': None
        },
        {
            'name': 'Simulated Stablecoin Data',
            'type': 'Stablecoin Supply',
            'description': 'Placeholder data - needs integration with DeFiLlama or similar',
            'status': '🔴 Simulated',
            'url': 'https://defillama.com/'
        }
    ]
    
    for source in sources:
        with st.expander(f"{source['status']} {source['name']}"):
            st.markdown(f"**Type**: {source['type']}")
            st.markdown(f"**Description**: {source['description']}")
            if source['url']:
                st.markdown(f"**URL**: [{source['url']}]({source['url']})")
    
    st.markdown("---")
    
    st.markdown("""
    ## Recommended Additional Data Sources
    
    To fully implement the corruption index thesis, consider integrating:
    
    ### Real-Time Market Data
    - **Kaiko / CryptoCompare**: Professional-grade exchange data with geographic segmentation
    - **Glassnode / Chainalysis**: On-chain analytics and flow tracking
    - **DeFiLlama**: DeFi protocol TVL and stablecoin supplies
    - **LocalBitcoins / Paxful archives**: P2P premium data by country
    
    ### Policy & Economic Data
    - **OFAC Sanctions List API**: Real-time sanctions updates
    - **IMF / World Bank APIs**: Economic indicators, inflation, currency data
    - **Trading Economics**: Black market exchange rates
    - **GDELT Project**: News event tracking for policy announcements
    
    ### Alternative Indices
    - **Transparency International**: Corruption Perceptions Index
    - **Chinn-Ito Index**: Capital account openness
    - **TRACE Matrix**: Bribery risk by country
    - **Basel AML Index**: Anti-money laundering risk
    
    ## Methodology
    
    ### Corruption Index Calculation
    
    The composite index (0-100 scale) combines:
    
    1. **Volatility Component (30%)**: 30-day rolling standard deviation of prices
    2. **Volume Surge Component (30%)**: Z-score of trading volume vs 90-day average
    3. **Event Intensity Component (40%)**: Sum of policy event severity scores in 7-day windows
    
    ### Event Study Analysis
    
    For each policy event, we measure:
    - Price changes in [-30, +30] day windows
    - Volume surges in [0, +7] day windows
    - Cross-asset correlations during event periods
    
    ### Portfolio Optimization
    
    Expected returns are estimated from:
    - Historical crypto returns (2017-present)
    - Event-specific return patterns
    - Geographic exposure to policy friction
    - Leverage impact modeling
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## API Integration Guide
    
    To add new data sources, implement fetcher functions in the following pattern:
    
    ```python
    @st.cache_data(ttl=3600)
    def fetch_your_data(params):
        # Your API call here
        response = requests.get(url, params=params)
        return pd.DataFrame(response.json())
    ```
    
    Key principles:
    - Use `@st.cache_data` to avoid redundant API calls
    - Set appropriate TTL (time-to-live) for cache refresh
    - Return standardized pandas DataFrames
    - Handle errors gracefully with try/except
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Crypto Corruption Index Analysis Tool</p>
    <p style='font-size: 0.8rem;'>
        This tool is for research and educational purposes only. Not financial advice.
    </p>
</div>
""", unsafe_allow_html=True)
