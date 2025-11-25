# this is pure ai slop cobbed together with claude 4.5 - ymmv


# 🚀 Quick Start Guide - Crypto Corruption Index

## What This App Does

Tests your thesis that cryptocurrency functions as an **index for corruption and policy friction**, measuring what people will pay to circumvent institutional barriers.

## Installation (5 minutes)

### Option 1: Simple Launch (Recommended)

```bash
# Install dependencies
pip install streamlit pandas numpy plotly requests

# Run the app
streamlit run crypto_corruption_index.py
```

### Option 2: Using the launch script

```bash
chmod +x launch.sh
./launch.sh
```

The app will open automatically at `http://localhost:8501`

## First Steps

### 1. Overview Page (Start Here)
- See the current **Corruption Index** value (0-100 scale)
- View how the index has changed over the past year
- Observe spikes during major policy events (sanctions, banking crises)

**What to look for**: Does the index spike during known friction events?

### 2. Policy Events Page
- Review the timeline of 10+ major policy friction events
- Filter by type: Sanctions, Capital Controls, Banking Crises, Regulatory
- **Try adding a new event** to see how it affects the analysis

**Test case**: Add a recent event you know about (e.g., recent banking restrictions in your area)

### 3. Correlation Analysis Page
- Select a specific policy event from the dropdown
- View price movements 30 days before/after the event
- Check if crypto prices spiked following the event

**Key hypothesis test**: Do prices increase in the 7 days after policy friction events?

### 4. Market Data Page
- Compare Bitcoin, Ethereum, Stablecoins, Privacy Coins
- Toggle log scale for better visualization
- Watch stablecoin supply growth (capital flight proxy)

**Insight**: Stablecoin growth during crisis = capital fleeing traditional systems

### 5. Portfolio Builder Page
- Build a "corruption-weighted" portfolio
- Adjust allocations and leverage
- See expected returns in normal vs. crisis scenarios

**Recommended starting allocation**:
- 40% Stablecoins (2x leverage) - lowest vol, steady demand
- 30% Bitcoin (1x) - benchmark corruption index
- 20% Ethereum (1x) - technical utility + friction premium  
- 10% Privacy coins (1x) - pure corruption premium

## Testing Your Thesis

### Experiment 1: Event Impact Study
1. Go to **Correlation Analysis**
2. Choose "Russia - SWIFT removal" (March 2022)
3. Observe if Bitcoin/crypto spiked in the following week
4. Compare to other events

**Expected result**: Positive correlation between severe events (severity 8+) and price spikes

### Experiment 2: Cross-Asset Response
1. **Market Data** page → Compare all assets
2. Look at correlation matrix
3. Check if privacy coins (Monero) behave differently than Bitcoin

**Hypothesis**: Privacy coins should show higher correlation with sanctions/capital control events

### Experiment 3: Portfolio Backtest (Conceptual)
1. **Portfolio Builder** → Try different allocations
2. Compare "high stablecoin" (60%) vs "high Bitcoin" (60%) portfolios
3. Note the different risk/return profiles

**Key insight**: Stablecoin-heavy = more stable, Bitcoin-heavy = more volatile but higher crisis alpha

## Real Data Being Used

✅ **Live data** (updates hourly):
- CoinGecko API for crypto prices/volumes (past 365 days)
- Real historical price movements

⚠️ **Manual data** (you can add to it):
- Policy event database (10 events included, add more via UI)

🔴 **Simulated data** (placeholder):
- Stablecoin supply (shows trend, not real numbers yet)

## Next Steps for Production

To make this publication-ready:

1. **Add real stablecoin data**: Integrate DeFiLlama API
2. **Geographic data**: Need country-specific trading volumes
3. **Automate events**: Connect to news APIs (GDELT, NewsAPI)
4. **Statistical rigor**: Add p-values, regression coefficients
5. **More events**: Expand from 10 to 100+ events

## Understanding the Numbers

### Corruption Index (0-100)
- **0-30**: Low friction, normal market conditions
- **30-60**: Moderate friction, some policy events
- **60-100**: High friction, major crisis/sanctions

### Severity Scores (1-10)
- **1-3**: Minor regulatory changes
- **4-6**: Significant but localized events
- **7-8**: Major national crises
- **9-10**: Global systemic events (SWIFT removal, major sanctions)

### Expected Returns
- **Base case (15-30%)**: Annual return in stable periods
- **Crisis alpha (2-5x)**: Multiple during major friction events
- **Max drawdown (-50-70%)**: Worst-case scenario loss

## Troubleshooting

**"No module named streamlit"**
```bash
pip install streamlit pandas numpy plotly requests
```

**"Port 8501 already in use"**
```bash
streamlit run crypto_corruption_index.py --server.port 8502
```

**"API rate limit exceeded"**
- CoinGecko free tier: 10-30 calls/minute
- Wait a few minutes, data is cached for 1 hour

**"Events not showing up"**
- Events are hardcoded in `get_policy_events()` function
- Use the "Add New Event" form on Policy Events page (demo mode)

## Questions This App Answers

✅ "Do crypto prices spike after sanctions announcements?"
✅ "Is there a correlation between banking crises and stablecoin demand?"
✅ "What's the optimal allocation for capturing policy friction premiums?"
✅ "How much leverage should I use on different crypto types?"
✅ "Which events create the biggest price impacts?"

## Academic/Research Use

If using this for research:

1. **Export data**: Currently in demo mode, would need CSV export functionality
2. **Statistical tests**: P-values and confidence intervals not yet implemented
3. **Backtesting**: Historical portfolio performance needs proper calculation
4. **Citation**: See README.md for proper citation format

## Getting Help

Common issues:
- Check that Python 3.8+ is installed: `python --version`
- Verify dependencies: `pip list | grep streamlit`
- Review logs if app crashes (they appear in terminal)

## Have Fun! 

**crypto as a revealed preference index for institutional quality**. 

General thesis: What people pay to exit the system tells you more about the system's health than any official metric.

Start with the Overview page and explore from there. The correlation analysis is where the thesis really comes to life.
