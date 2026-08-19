"use client";

import { FormEvent, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type PortfolioItem = {
  asset: string;
  symbol: string;
  weight: number;
  amount: number;
};

type PrincipalSummary = {
  current_asset: number;
  future_contributions: number;
  total_principal: number;
};

type PortfolioResult = {
  risk_score: number;
  risk_grade: string;

  allocation: {
    stock: number;
    bond: number;
    cash: number;
  };

  investment_plan: PortfolioItem[];
  current_asset_plan: PortfolioItem[];
  principal_summary: PrincipalSummary;

  yearly_projection: {
    year: number;
    asset: number;
  }[];

  future_simulation: {
    annual_return: number;
    future_value: number;
    total_principal: number;
    investment_profit: number;
  };
};

export default function Home() {
  const [age, setAge] = useState(28);
  const [currentAsset, setCurrentAsset] = useState(30000000);
  const [monthlyInvestment, setMonthlyInvestment] = useState(1000000);
  const [investmentYears, setInvestmentYears] = useState(10);
  const [riskLevel, setRiskLevel] = useState("balanced");

  const [result, setResult] = useState<PortfolioResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/portfolio", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          age,
          current_asset: currentAsset,
          monthly_investment: monthlyInvestment,
          investment_years: investmentYears,
          risk_level: riskLevel,
        }),
      });

      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-12">
      <div className="mx-auto max-w-6xl">
        <div className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900">AssetFlow</h1>
          <p className="mt-2 text-gray-600">
            내 투자 조건에 맞는 자산배분을 시뮬레이션해보세요.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[360px_1fr]">
          <form
            onSubmit={handleSubmit}
            className="h-fit rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="mb-6 text-xl font-semibold text-gray-900">
              투자 정보
            </h2>

            <div className="space-y-5">
              <label className="block">
                <span className="text-sm font-medium text-gray-700">나이</span>
                <input
                  type="number"
                  value={age}
                  onChange={(e) => setAge(Number(e.target.value))}
                  className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-700">
                  현재 금융자산
                </span>
                <input
                  type="number"
                  value={currentAsset}
                  onChange={(e) => setCurrentAsset(Number(e.target.value))}
                  className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-700">
                  월 투자금
                </span>
                <input
                  type="number"
                  value={monthlyInvestment}
                  onChange={(e) =>
                    setMonthlyInvestment(Number(e.target.value))
                  }
                  className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-700">
                  투자 기간
                </span>
                <input
                  type="number"
                  value={investmentYears}
                  onChange={(e) =>
                    setInvestmentYears(Number(e.target.value))
                  }
                  className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-700">
                  위험 성향
                </span>
                <select
                  value={riskLevel}
                  onChange={(e) => setRiskLevel(e.target.value)}
                  className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2"
                >
                  <option value="conservative">보수적</option>
                  <option value="balanced">균형형</option>
                  <option value="aggressive">공격적</option>
                </select>
              </label>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-black px-4 py-3 font-semibold text-white"
              >
                {loading ? "계산 중..." : "자산배분 계산하기"}
              </button>
            </div>
          </form>

          <section className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="mb-6 text-xl font-semibold text-gray-900">
              분석 결과
            </h2>

            {!result ? (
              <p className="text-gray-500">
                투자 정보를 입력하고 계산 버튼을 눌러주세요.
              </p>
            ) : (
              <div className="space-y-8">
                <div>
                  <div className="mb-4 rounded-xl bg-gray-50 p-4">
                    <p className="text-sm text-gray-500">위험 점수</p>
                    <p className="text-3xl font-bold">
                      {result.risk_score} / 100
                    </p>
                    <p className="mt-1 text-sm text-gray-600">
                      {result.risk_grade}
                    </p>
                  </div>

                  <div className="grid grid-cols-3 gap-3">
                    <div className="rounded-lg bg-gray-50 p-3 text-center">
                      <p className="text-sm text-gray-500">주식</p>
                      <p className="text-xl font-bold">
                        {result.allocation.stock}%
                      </p>
                    </div>

                    <div className="rounded-lg bg-gray-50 p-3 text-center">
                      <p className="text-sm text-gray-500">채권</p>
                      <p className="text-xl font-bold">
                        {result.allocation.bond}%
                      </p>
                    </div>

                    <div className="rounded-lg bg-gray-50 p-3 text-center">
                      <p className="text-sm text-gray-500">현금</p>
                      <p className="text-xl font-bold">
                        {result.allocation.cash}%
                      </p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="mb-3 font-semibold">투자 원금 요약</h3>

                  <div className="grid gap-3 sm:grid-cols-3">
                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">현재 자산</p>
                      <p className="mt-1 font-bold">
                        {result.principal_summary.current_asset.toLocaleString()}
                        원
                      </p>
                    </div>

                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">향후 납입액</p>
                      <p className="mt-1 font-bold">
                        {result.principal_summary.future_contributions.toLocaleString()}
                        원
                      </p>
                    </div>

                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">총 투자원금</p>
                      <p className="mt-1 font-bold">
                        {result.principal_summary.total_principal.toLocaleString()}
                        원
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid gap-8 md:grid-cols-2">
                  <div>
                    <h3 className="mb-3 font-semibold">현재 자산 배분</h3>

                    <div className="space-y-3">
                      {result.current_asset_plan.map((item) => (
                        <div
                          key={item.symbol}
                          className="flex items-center justify-between border-b border-gray-100 pb-3"
                        >
                          <div>
                            <p className="font-medium">{item.asset}</p>
                            <p className="text-sm text-gray-500">
                              {item.weight}%
                            </p>
                          </div>

                          <p className="font-semibold">
                            {item.amount.toLocaleString()}원
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h3 className="mb-3 font-semibold">월 투자 계획</h3>

                    <div className="space-y-3">
                      {result.investment_plan.map((item) => (
                        <div
                          key={item.symbol}
                          className="flex items-center justify-between border-b border-gray-100 pb-3"
                        >
                          <div>
                            <p className="font-medium">{item.asset}</p>
                            <p className="text-sm text-gray-500">
                              {item.weight}%
                            </p>
                          </div>

                          <p className="font-semibold">
                            {item.amount.toLocaleString()}원
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="mb-3 font-semibold">미래 자산 시뮬레이션</h3>

                  <div className="grid gap-3 sm:grid-cols-3">
                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">
                        {investmentYears}년 후 예상 자산
                      </p>
                      <p className="mt-1 text-lg font-bold">
                        {result.future_simulation.future_value.toLocaleString()}원
                      </p>
                    </div>

                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">총 투자원금</p>
                      <p className="mt-1 text-lg font-bold">
                        {result.future_simulation.total_principal.toLocaleString()}원
                      </p>
                    </div>

                    <div className="rounded-xl bg-gray-50 p-4">
                      <p className="text-sm text-gray-500">예상 투자수익</p>
                      <p className="mt-1 text-lg font-bold">
                        +{result.future_simulation.investment_profit.toLocaleString()}원
                      </p>
                    </div>
                  </div>

                  <p className="mt-3 text-xs text-gray-500">
                    연 {(result.future_simulation.annual_return * 100).toFixed(1)}% 수익률을
                    가정한 시뮬레이션입니다.
                  </p>
                </div>
                
                <div>
                    <h3 className="mb-4 font-semibold">예상 자산 성장</h3>

                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={result.yearly_projection}>
                          <CartesianGrid strokeDasharray="3 3" />

                          <XAxis
                            dataKey="year"
                            tickFormatter={(value) => `${value}년`}
                          />

                          <YAxis
                            tickFormatter={(value) => {
                              const eok = value / 100000000;
                              return `${Number(eok.toFixed(1))}억`;
                            }}
                          />

                          <Tooltip
                            formatter={(value) =>
                              `${Number(value).toLocaleString()}원`
                            }
                            labelFormatter={(label) => `${label}년`}
                          />

                          <Line
                            type="monotone"
                            dataKey="asset"
                            strokeWidth={2}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>      
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}