import axios from "axios";

// Define the types for transactions and the summary response
export interface Transaction {
  txId: string;
  fee_in_usdt: number;
  fee_in_eth: number;
}

export interface Summary {
  total_usdt_fees: number;
  total_eth_fees: number;
  eth_usdt_price: number;
}

// Axios instance to simplify repeated configuration
const API_BASE_URL = "http://localhost:8000"; // Adjust as necessary
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

// Fetch transactions by transaction ID
export const fetchTransactionByTxId = async (
  txId: string
): Promise<Transaction> => {
  const response = await axiosInstance.get(`/transactions/${txId}`);
  return response.data;
};

// Fetch transactions by time range
export const fetchTransactionsByTimeRange = async (
  start: string,
  end: string,
  page = 1,
  limit = 50
): Promise<{ transactions: Transaction[] }> => {
  const response = await axiosInstance.get("/transactions", {
    params: {
      start_time: start,
      end_time: end,
      page,
      limit,
    },
  });
  return response.data;
};

// Fetch summary (total fees and current ETH/USDT price)
export const fetchSummary = async (): Promise<Summary> => {
  const response = await axiosInstance.get("/summary");
  return response.data;
};