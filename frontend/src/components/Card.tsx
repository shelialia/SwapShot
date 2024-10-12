import React, { useState, useEffect } from "react";
import { Transaction } from "../services/api";
import { fetchExchangeRate as getExchangeRateFromAPI } from "../services/api"; // Rename imported function

interface Props {
  transaction: Transaction | null;
}

const TransactionCard: React.FC<Props> = ({ transaction }) => {
  const [exchangeRate, setExchangeRate] = useState<number | null>(null); // State to store exchange rate

  // Fetch the exchange rate when the transaction is selected
  useEffect(() => {
    const fetchRate = async () => {
      if (transaction) {
        // Only fetch if a transaction is selected
        try {
          const data = await getExchangeRateFromAPI(); // Use the correctly imported function
          setExchangeRate(data); // Make sure the correct field is accessed
        } catch (error) {
          console.error("Error fetching exchange rate:", error);
        }
      }
    };

    fetchRate();
  }, [transaction]); // Run whenever the selected transaction changes

  if (!transaction) {
    return (
      <div className="border border-gray-300 rounded-lg p-4">
        <h2 className="text-xl font-semibold">No Transaction Selected</h2>
        <p>Select a transaction ID to view details.</p>
      </div>
    );
  }

  const epochTime = Number(transaction.timeStamp) * 1000; // multiply by 1000 if in seconds
  const humanReadableTime = new Date(epochTime).toLocaleString(); // Convert to human-readable time

  return (
    <div className="border border-gray-300 rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Transaction Details</h2>
      <p>
        <strong>Tx ID:</strong> {transaction.txId}
      </p>
      <p>
        <strong>Transaction Time</strong> {humanReadableTime}
      </p>
      <p>
        <strong>Fee in ETH:</strong> {transaction.fee_in_eth}
      </p>
      <p>
        <strong>Fee in USDT:</strong> {transaction.fee_in_usdt}
      </p>
      <p>
        <strong>Historical Exchange Rate (ETH/USDT):</strong>{" "}
        {transaction.eth_usdt_price}
      </p>

      {/* Display exchange rate or fallback */}
      {exchangeRate !== null ? (
        <p>
          <strong>Current Exchange Rate (ETH/USDT): </strong> {exchangeRate}
        </p>
      ) : (
        <p>Loading exchange rate...</p>
      )}
    </div>
  );
};

export default TransactionCard;
