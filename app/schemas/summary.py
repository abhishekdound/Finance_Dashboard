from pydantic import BaseModel
from typing import List, Dict

from app.schemas.record import Record


class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: Dict[str, float]
    recent_activity: List[Record]
