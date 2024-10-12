import axios from 'axios';

// Define the types for transactions and the summary response
export interface Transaction {
  txId: string;
  timeStamp: string;
  eth_usdt_price: number;
  fee_in_usdt: number;
  fee_in_eth: number;
}

export interface Summary {
  total_usdt_fees: number;
  total_eth_fees: number;
  eth_usdt_price: number;
}

// Axios instance to simplify repeated configuration
const API_BASE_URL = "http://127.0.0.1:8000";  // Adjust as necessary
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

// Fetch transactions by transaction ID
export const fetchTransactionByTxId = async (txId: string): Promise<Transaction> => {
    console.log(txId)
    const response = await axiosInstance.get(`/transactions/${txId}`);
    console.log(response.data)
  return response.data;
};

// Fetch transactions by time range
export const fetchTransactionsByTimeRange = async (
  start: string,
  end: string,
  page = 1,
  limit = 100
): Promise<{ transactions: Transaction[]; total: number }> => {
  const startUnix = Math.floor(new Date(start).getTime() / 1000); // Convert to Unix timestamp
  const endUnix = Math.floor(new Date(end).getTime() / 1000); // Convert to Unix timestamp
    console.log(startUnix)
    console.log(endUnix)
  const response = await axiosInstance.get(`/transaction/${startUnix}/${endUnix}/${page}/${limit}`);
    console.log("txn in time interval")
    console.log(response.data);

  return response.data;
};

// Fetch all transactions (paginated) using axios
export const fetchAllTransactions = async (
  page: number,
  limit: number
): Promise<{ transactions: Transaction[]; total: number }> => {
    try {
        console.log("Hi")
    const response = await axiosInstance.get(`/all_transactions/${page}/${limit}`);
    console.log(response.data); // Log response for debugging
    return response.data; // Return the parsed JSON response
  } catch (error) {
    console.error("Failed to fetch all transactions:", error);
    throw new Error("Failed to fetch all transactions");
  }
};

export const fetchExchangeRate = async (): Promise<{ rate: number }> => {
    try {
        const response = await axiosInstance.get('exchange_rate');
        console.log(response);
        return response.data;
    } catch (error) {
        console.error("Failed to fetch exchange rate:", error);
        throw new Error("Failed to get exchange rate");
    }
};
