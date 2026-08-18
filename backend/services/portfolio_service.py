from models.portfolio import PortfolioRequest


def calculate_portfolio(request: PortfolioRequest):
    risk_score_map = {
        "conservative": 30,
        "balanced": 60,
        "aggressive": 80,
    }

    risk_score = risk_score_map.get(request.risk_level, 50)

    if request.age < 30:
        risk_score += 10
    elif request.age < 40:
        risk_score += 5
    elif request.age >= 60:
        risk_score -= 10

    if request.investment_years >= 10:
        risk_score += 10
    elif request.investment_years >= 5:
        risk_score += 5
    elif request.investment_years <= 2:
        risk_score -= 10

    risk_score = max(0, min(risk_score, 100))

    if risk_score >= 70:
        risk_grade = "aggressive"
        allocation = {
            "stock": 80,
            "bond": 15,
            "cash": 5,
        }

    elif risk_score >= 40:
        risk_grade = "balanced"
        allocation = {
            "stock": 60,
            "bond": 30,
            "cash": 10,
        }

    else:
        risk_grade = "conservative"
        allocation = {
            "stock": 30,
            "bond": 50,
            "cash": 20,
        }

    return {
        "age": request.age,
        "current_asset": request.current_asset,
        "monthly_investment": request.monthly_investment,
        "investment_years": request.investment_years,
        "risk_level": request.risk_level,
        "risk_score": risk_score,
        "risk_grade": risk_grade,
        "allocation": allocation,
    }