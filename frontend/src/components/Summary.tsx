import React from "react";
import { Summary } from "../services/api";

interface Props {
  summary: Summary | null;
}

const SummaryComponent: React.FC<Props> = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="mt-8 p-4 border rounded-lg shadow-md bg-gray-50">
      <h2 className="text-xl font-semibold mb-2">Transaction Summary</h2>
      <p className="mb-2">
        Total Transaction Fee in USDT:{" "}
        <span className="font-bold">{summary.total_usdt_fees}</span>
      </p>
      <p className="mb-2">
        Total Transaction Fee in ETH:{" "}
        <span className="font-bold">{summary.total_eth_fees}</span>
      </p>
      <p className="mb-2">
        Current ETH/USDT Price:{" "}
        <span className="font-bold">{summary.eth_usdt_price}</span>
      </p>
    </div>
  );
};

export default SummaryComponent;
