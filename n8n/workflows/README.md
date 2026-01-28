# n8n Workflow Templates

This folder contains ready-to-import n8n workflow templates for investment professionals and content automation.

## Workflows Included

### 1. Content Generation Pipeline (`content_generation.json`)
Automates the Substack → Social Content pipeline:
- Triggers weekly or on-demand
- Runs the content-agent CLI
- Reads generated JSON output
- Optionally sends to Notion/Slack for review

### 2. Earnings Calendar Monitor (`earnings_calendar_monitor.json`)
For investment professionals:
- Monitors earnings calendars for selected stocks
- Sends alerts before earnings calls
- Integrates with your preferred notification channel (Slack, Email, Telegram)

### 3. SEC Filing Alerts (`sec_filing_alerts.json`)
- Monitors SEC EDGAR for new 8-K, 10-K, 10-Q filings
- Filters by company watchlist
- Sends immediate alerts with filing summaries

### 4. Stock Price Alert System (`stock_price_alerts.json`)
- Monitors price movements and technical indicators
- Customizable threshold alerts
- Integrates with trading platforms or notification systems

### 5. Financial News Aggregator (`financial_news_aggregator.json`)
- Aggregates news from multiple financial sources
- AI-powered relevance filtering
- Daily digest or real-time alerts

### 6. Portfolio Performance Tracker (`portfolio_tracker.json`)
- Tracks portfolio performance
- Generates daily/weekly reports
- Calculates key metrics (P&L, allocation, risk metrics)

## How to Import

1. Open your n8n instance
2. Go to Workflows → Import from File
3. Select the JSON file you want to import
4. Configure credentials (API keys, etc.)
5. Activate the workflow

## Configuration Required

Most workflows require you to configure:
- API credentials (financial data providers, notification services)
- Watchlist of tickers/companies
- Notification preferences
- Schedule/timing preferences

See individual workflow documentation for specific requirements.
