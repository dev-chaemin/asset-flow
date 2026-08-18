from fastapi import FastAPI

from models.portfolio import PortfolioRequest
from services.portfolio_service import calculate_portfolio

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "AssetFlow API is running"}


@app.post("/portfolio")
def create_portfolio(request: PortfolioRequest):
    return calculate_portfolio(request)