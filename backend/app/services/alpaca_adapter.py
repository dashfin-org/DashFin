import os
import httpx
from datetime import datetime, timedelta
from typing import List, Dict

ALPACA_KEY = os.getenv("ALPACA_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")
ALPACA_DOMAIN = os.getenv("ALPACA_DOMAIN", "https://paper-api.alpaca.markets")

class AlpacaAdapter:
    def __init__(self):
        self.headers = {
            "APCA-API-KEY-ID": ALPACA_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET,
        }
        self.base = ALPACA_DOMAIN

    async def get_account(self) -> Dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base}/v2/account", headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def get_positions(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base}/v2/positions", headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def get_history(self, days: int = 30) -> List[Dict]:
        until = datetime.utcnow()
        since = until - timedelta(days=days)
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.base}/v2/account/portfolio/history",
                headers=self.headers,
                params={"start": since.isoformat(), "end": until.isoformat(), "period": "1D"},
            )
            r.raise_for_status()
            return r.json().get("equity", [])
