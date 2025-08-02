# DashFin
# DashFin

**DashFin** is a modular, full-stack, professional finance dashboard and analytics suite.

## Key Features
- Advanced charting, real-time news, and sentiment scoring
- Multi-broker portfolio management and risk analytics
- Macroeconomic data and historical trend analysis
- AI-driven backtesting, hypothesis lab, custom indicator builder
- Integrated with Alpaca, FRED, Yahoo, Alpha Vantage, Polygon, and more
- Responsive dark-mode UI with drag-and-drop widgets

## Quick Start

This repo contains the core monorepo structure:
- `/frontend` - React/TypeScript finance dashboard UI
- `/backend` - FastAPI + Python analytics API server
- `/devops` - Docker, cloud build, and CI configs
- `/docs` - Architecture and developer docs

**Work in progress.** See `/docs/` for system overview.

## License

© 2025 DashFin. All rights reserved.

## 📦 Alpaca Integration

### What's added:
- Backend `AlpacaAdapter` for portfolio and account history
- API endpoint: `GET /api/v1/portfolio/alpaca/history`
- Frontend `PortfolioAlpacaWidget` fetching live data
- Unit tests using FastAPI test client and mocking
- `.env.example` updated with Alpaca keys

### How to test:
1. Add your Alpaca credentials to `.env`
2. Run backend: `uvicorn app.main:app --reload`
3. Visit `/api/v1/portfolio/alpaca/history` for JSON response
4. Launch frontend; the new widget fetches and displays data

Feel free to review and merge to enable further adapter integration.


## Project badges
(markdown badges TBD)
