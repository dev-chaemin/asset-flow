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
    
def calculate_investment_amounts(
    portfolio: list,
    monthly_investment: int,
):
    result = []

    for item in portfolio:
        amount = monthly_investment * item["weight"] / 100

        result.append({
            **item,
            "amount": int(amount),
        })

    return result


def calculate_current_asset_allocation(
    portfolio: list,
    current_asset: int,
):
    result = []

    for item in portfolio:
        amount = current_asset * item["weight"] / 100

        result.append({
            **item,
            "amount": int(amount),
        })

    return result


def calculate_principal_summary(
    current_asset: int,
    monthly_investment: int,
    investment_years: int,
):
    future_contributions = (
        monthly_investment
        * 12
        * investment_years
    )

    total_principal = current_asset + future_contributions

    return {
        "current_asset": current_asset,
        "future_contributions": future_contributions,
        "total_principal": total_principal,
    }


def get_expected_annual_return(risk_grade: str):
    expected_return_map = {
        "conservative": 0.04,
        "balanced": 0.06,
        "aggressive": 0.08,
    }

    return expected_return_map[risk_grade]


def simulate_future_value(
    current_asset: int,
    monthly_investment: int,
    investment_years: int,
    annual_return: float,
):
    monthly_return = annual_return / 12
    total_months = investment_years * 12

    future_current_asset = current_asset * (
        (1 + monthly_return) ** total_months
    )

    future_contributions = 0

    for month in range(total_months):
        remaining_months = total_months - month

        future_contributions += monthly_investment * (
            (1 + monthly_return) ** remaining_months
        )

    future_value = future_current_asset + future_contributions

    total_principal = (
        current_asset
        + monthly_investment * total_months
    )

    investment_profit = future_value - total_principal

    return {
        "annual_return": annual_return,
        "future_value": int(future_value),
        "total_principal": total_principal,
        "investment_profit": int(investment_profit),
    }


def create_yearly_projection(
    current_asset: int,
    monthly_investment: int,
    investment_years: int,
    annual_return: float,
):
    monthly_return = annual_return / 12
    current_value = current_asset

    projection = [
        {
            "year": 0,
            "asset": int(current_value),
        }
    ]

    for month in range(1, investment_years * 12 + 1):
        current_value *= (1 + monthly_return)
        current_value += monthly_investment

        if month % 12 == 0:
            projection.append({
                "year": month // 12,
                "asset": int(current_value),
            })

    return projection


def calculate_portfolio(request: PortfolioRequest):
    risk_score = calculate_risk_score(request)
    risk_grade = determine_risk_grade(risk_score)
    allocation = create_allocation(risk_grade)
    portfolio = create_portfolio(risk_grade)

    investment_plan = calculate_investment_amounts(
        portfolio,
        request.monthly_investment,
    )

    current_asset_plan = calculate_current_asset_allocation(
        portfolio,
        request.current_asset,
    )

    principal_summary = calculate_principal_summary(
        request.current_asset,
        request.monthly_investment,
        request.investment_years,
    )

    annual_return = get_expected_annual_return(risk_grade)

    future_simulation = simulate_future_value(
        request.current_asset,
        request.monthly_investment,
        request.investment_years,
        annual_return,
    )

    yearly_projection = create_yearly_projection(
        request.current_asset,
        request.monthly_investment,
        request.investment_years,
        annual_return,
    )
    
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
        "investment_plan": investment_plan,
        "current_asset_plan": current_asset_plan,
        "principal_summary": principal_summary,
        "future_simulation": future_simulation,
        "yearly_projection": yearly_projection,
    }