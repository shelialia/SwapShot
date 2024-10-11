import React, { useState, useEffect } from "react";
import TransactionTable from "../components/TransactionTable";
import SummaryComponent from "../components/Summary";
import {
  fetchTransactionByTxId,
  fetchTransactionsByTimeRange,
  fetchSummary,
  Transaction,
  Summary,
} from "../services/api";

const TransactionsPage: React.FC = () => {
  const [txId, setTxId] = useState<string>("");
  const [startTime, setStartTime] = useState<string>("");
  const [endTime, setEndTime] = useState<string>("");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(50);

  const handleSearchByTxId = async () => {
    try {
      const data = await fetchTransactionByTxId(txId);
      setTransactions([data]);
    } catch (error) {
      console.error("Error fetching transaction:", error);
    }
  };

  const handleSearchByTimeRange = async () => {
    try {
      const data = await fetchTransactionsByTimeRange(
        startTime,
        endTime,
        page,
        pageSize
      );
      setTransactions(data.transactions);
    } catch (error) {
      console.error("Error fetching transactions by time range:", error);
    }
  };

  const loadSummary = async () => {
    try {
      const summaryData = await fetchSummary();
      setSummary(summaryData);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  useEffect(() => {
    loadSummary(); // Load the summary when the component mounts
  }, []);

    return (
      <div className="py-8 px-8">
        <h1 className="text-3xl font-bold mb-4">Transaction Search</h1>

        {/* Search by Transaction ID */}
        <div className="flex flex-row">
          <input
            type="text"
            placeholder="Search by Transaction ID"
            value={txId}
            onChange={(e) => setTxId(e.target.value)}
            className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
          />
          <button
            onClick={handleSearchByTxId}
            className="bg-blue-500 text-white font-semibold whitespace-nowrap px-4 py-2 ml-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
          >
            Search by Tx ID
          </button>
        </div>

        {/* Search by Time Range */}
        <div className="flex flex-row space-x-4 items-center mt-4">
          <input
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearchByTimeRange}
            className="bg-blue-500 text-white font-semibold px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300 whitespace-nowrap"
          >
            Search by Time Range
          </button>
        </div>

        {/* Transaction Table */}
        <TransactionTable
          transactions={transactions}
          page={page}
          setPage={setPage}
          pageSize={pageSize}
          setPageSize={setPageSize}
        />

        {/* Summary Component */}
        <SummaryComponent summary={summary} />
      </div>
    );
};

export default TransactionsPage;