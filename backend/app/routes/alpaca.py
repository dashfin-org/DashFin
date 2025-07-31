from fastapi import APIRouter, Depends, HTTPException
from app.auth.oauth_handler import get_current_user
from app.services.alpaca_adapter import AlpacaAdapter

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])

@router.get("/alpaca/history")
async def alpaca_history(user = Depends(get_current_user)):
    try:
        adapter = AlpacaAdapter()
        equity = await adapter.get_history(days=30)
        metrics = await adapter.get_account()
        return {"equity": equity, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
