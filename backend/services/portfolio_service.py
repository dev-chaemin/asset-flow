from models.portfolio import PortfolioRequest


def calculate_risk_score(request: PortfolioRequest):
    risk_score_map = {
        "conservative": 30,
        "balanced": 60,
        "aggressive": 80,
    }

    risk_score = risk_score_map.get(request.risk_level, 50)

    # 나이에 따른 위험 점수 보정
    if request.age < 30:
        risk_score += 10
    elif request.age < 40:
        risk_score += 5
    elif request.age >= 60:
        risk_score -= 10

    # 투자 기간에 따른 위험 점수 보정
    if request.investment_years >= 10:
        risk_score += 10
    elif request.investment_years >= 5:
        risk_score += 5
    elif request.investment_years <= 2:
        risk_score -= 10

    return max(0, min(risk_score, 100))


def determine_risk_grade(risk_score: int):
    if risk_score >= 70:
        return "aggressive"
    elif risk_score >= 40:
        return "balanced"
    else:
        return "conservative"


def create_allocation(risk_grade: str):
    if risk_grade == "aggressive":
        return {
            "stock": 80,
            "bond": 15,
            "cash": 5,
        }

    elif risk_grade == "balanced":
        return {
            "stock": 60,
            "bond": 30,
            "cash": 10,
        }

    else:
        return {
            "stock": 30,
            "bond": 50,
            "cash": 20,
        }


def create_portfolio(risk_grade: str):
    if risk_grade == "aggressive":
        return [
            {"asset": "US Large Cap", "symbol": "US_LARGE_CAP", "weight": 40},
            {"asset": "US Growth", "symbol": "US_GROWTH", "weight": 25},
            {"asset": "International Stock", "symbol": "INTL_STOCK", "weight": 15},
            {"asset": "Bond", "symbol": "BOND", "weight": 15},
            {"asset": "Cash", "symbol": "CASH", "weight": 5},
        ]

    elif risk_grade == "balanced":
        return [
            {"asset": "US Large Cap", "symbol": "US_LARGE_CAP", "weight": 35},
            {"asset": "International Stock", "symbol": "INTL_STOCK", "weight": 25},
            {"asset": "Bond", "symbol": "BOND", "weight": 30},
            {"asset": "Cash", "symbol": "CASH", "weight": 10},
        ]

    else:
        return [
            {"asset": "US Large Cap", "symbol": "US_LARGE_CAP", "weight": 20},
            {"asset": "International Stock", "symbol": "INTL_STOCK", "weight": 10},
            {"asset": "Bond", "symbol": "BOND", "weight": 50},
            {"asset": "Cash", "symbol": "CASH", "weight": 20},
        ]


def calculate_portfolio(request: PortfolioRequest):
    risk_score = calculate_risk_score(request)
    risk_grade = determine_risk_grade(risk_score)
    allocation = create_allocation(risk_grade)
    portfolio = create_portfolio(risk_grade)

    return {
        "age": request.age,
        "current_asset": request.current_asset,
        "monthly_investment": request.monthly_investment,
        "investment_years": request.investment_years,
        "risk_level": request.risk_level,
        "risk_score": risk_score,
        "risk_grade": risk_grade,
        "allocation": allocation,
        "portfolio": portfolio,
    }