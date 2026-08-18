from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PortfolioRequest(BaseModel):
    age: int
    current_asset: int
    monthly_investment: int
    investment_years: int
    risk_level: str


@app.get("/")
def read_root():
    return {"message": "AssetFlow API is running"}


@app.post("/portfolio")
def create_portfolio(request: PortfolioRequest):

    if request.risk_level == "conservative":
        allocation = {
            "stock": 30,
            "bond": 50,
            "cash": 20
        }

    elif request.risk_level == "balanced":
        allocation = {
            "stock": 60,
            "bond": 30,
            "cash": 10
        }

    elif request.risk_level == "aggressive":
        allocation = {
            "stock": 80,
            "bond": 15,
            "cash": 5
        }

    else:
        allocation = {
            "stock": 50,
            "bond": 30,
            "cash": 20
        }

    return {
        "age": request.age,
        "current_asset": request.current_asset,
        "monthly_investment": request.monthly_investment,
        "investment_years": request.investment_years,
        "risk_level": request.risk_level,
        "allocation": allocation
    }