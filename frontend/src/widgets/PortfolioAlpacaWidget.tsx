import React, { useEffect, useState } from "react";

interface HistoryPoint { date: string; value: number; }

const PortfolioAlpacaWidget: React.FC = () => {
  const [equity, setEquity] = useState<HistoryPoint[]>([]);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    fetch("/api/v1/portfolio/alpaca/history")
      .then(res => res.json())
      .then(data => {
        setEquity(data.equity || []);
        setMetrics(data.metrics || {});
      });
  }, []);

  return (
    <div className="widget">
      <h3>Portfolio (Alpaca)</h3>
      {metrics && <div>Equity: ${metrics.equity}</div>}
      <div className="chart-placeholder">
        {equity.length > 0 ? "[Chart placeholder]" : "No data"}
      </div>
    </div>
  );
};

export default PortfolioAlpacaWidget;
