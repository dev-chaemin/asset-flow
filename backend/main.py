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

    # 1. 위험성향 기본 점수
    risk_score_map = {
        "conservative": 30,
        "balanced": 60,
        "aggressive": 80,
    }

    risk_score = risk_score_map.get(request.risk_level, 50)

    # 2. 나이에 따른 보정
    if request.age < 30:
        risk_score += 10
    elif request.age < 40:
        risk_score += 5
    elif request.age >= 60:
        risk_score -= 10

    # 3. 투자기간에 따른 보정
    if request.investment_years >= 10:
        risk_score += 10
    elif request.investment_years >= 5:
        risk_score += 5
    elif request.investment_years <= 2:
        risk_score -= 10

    # 4. 점수 범위 제한
    risk_score = max(0, min(risk_score, 100))

    # 5. 최종 점수에 따른 자산배분
    if risk_score >= 70:
        risk_grade = "aggressive"
        allocation = {
            "stock": 80,
            "bond": 15,
            "cash": 5
        }

    elif risk_score >= 40:
        risk_grade = "balanced"
        allocation = {
            "stock": 60,
            "bond": 30,
            "cash": 10
        }

    else:
        risk_grade = "conservative"
        allocation = {
            "stock": 30,
            "bond": 50,
            "cash": 20
        }

    return {
        "age": request.age,
        "current_asset": request.current_asset,
        "monthly_investment": request.monthly_investment,
        "investment_years": request.investment_years,
        "risk_level": request.risk_level,
        "risk_score": risk_score,
        "risk_grade": risk_grade,
        "allocation": allocation
    }