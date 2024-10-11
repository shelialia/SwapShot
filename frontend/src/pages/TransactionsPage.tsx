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
import { Button, TextField } from "@mui/material";

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
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Transaction Search</h1>

      {/* Search by Transaction ID */}
      <div className="mb-4">
        <TextField
          label="Transaction ID"
          variant="outlined"
          value={txId}
          onChange={(e) => setTxId(e.target.value)}
          className="mr-2"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSearchByTxId}
        >
          Search by Tx ID
        </Button>
      </div>

      {/* Search by Time Range */}
      <div className="mb-4 flex space-x-4">
        <TextField
          label="Start Time"
          type="datetime-local"
          InputLabelProps={{ shrink: true }}
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          className="mr-2"
        />
        <TextField
          label="End Time"
          type="datetime-local"
          InputLabelProps={{ shrink: true }}
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          className="mr-2"
        />
        <Button
          variant="contained"
          color="secondary"
          onClick={handleSearchByTimeRange}
        >
          Search by Time Range
        </Button>
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
