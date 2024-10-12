import React, { useState, useEffect } from "react";
import TransactionTable from "../components/TransactionTable";
import {
  fetchTransactionByTxId,
  fetchTransactionsByTimeRange,
  Transaction,
  fetchAllTransactions,
} from "../services/api";
import TransactionCard from "../components/Card";

const TransactionsPage: React.FC = () => {
  const [txId, setTxId] = useState<string>("");
  const [startTime, setStartTime] = useState<string>("");
  const [endTime, setEndTime] = useState<string>("");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(50);
    const [total, setTotal] = useState<number>(0);
    const [selectedTransaction, setSelectedTransaction] =
      useState<Transaction | null>(null);

    const handleTransactionClick = async (txId: string) => {
      try {
        const data = await fetchTransactionByTxId(txId);
        setSelectedTransaction(data); // Set the selected transaction
      } catch (error) {
        console.error("Error fetching transaction details:", error);
      }
    };

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
      console.log("trying to fetch data");
      const data = await fetchTransactionsByTimeRange(
        startTime,
        endTime,
        page,
        pageSize
      );
      setTransactions(data.transactions); // Set transactions
      setTotal(data.total); // Set total from the API response
    } catch (error) {
      console.error("Error fetching transactions by time range:", error);
    }
  };

  const loadAllTransactions = async () => {
      try {
        console.log("Hi I am trying")
          const data = await fetchAllTransactions(page, pageSize); // Fetch transactions with page and pageSize
          console.log(data)
      setTransactions(data.transactions); // Set transactions
        setTotal(data.total); // Set total from the API response
        console.log(data.transactions);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  // Trigger API call whenever page or pageSize changes
  useEffect(() => {
    loadAllTransactions();
  }, [page, pageSize]); // Re-run the effect when page or pageSize changes

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

      <div className="flex flex-row mt-8">
        {/* Right side: Transaction Table */}
        <div className="w-1/2">
          <h1 className="text-3xl font-bold mb-4 text-xl">Transaction IDs</h1>
          <TransactionTable
            transactions={transactions}
            page={page}
            setPage={setPage}
            pageSize={pageSize}
            setPageSize={setPageSize}
            total={total}
            onTransactionClick={handleTransactionClick} // Pass the click handler
          />
        </div>

        {/* Right side: Transaction Details Card */}
        <div className="w-1/2 ml-8 mt-12">
          <TransactionCard transaction={selectedTransaction} />
        </div>
      </div>
    </div>
  );
};

export default TransactionsPage;
