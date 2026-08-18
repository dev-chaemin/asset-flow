from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.portfolio import PortfolioRequest
from services.portfolio_service import calculate_portfolio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "AssetFlow API is running"}


@app.post("/portfolio")
def create_portfolio(request: PortfolioRequest):
    return calculate_portfolio(request)