from pydantic import BaseModel


class PortfolioRequest(BaseModel):
    age: int
    current_asset: int
    monthly_investment: int
    investment_years: int
    risk_level: str