import React from "react";
import { Pagination } from "@mui/material";
import { Transaction } from "../services/api";

interface Props {
  transactions: Transaction[];
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
  pageSize: number;
  setPageSize: React.Dispatch<React.SetStateAction<number>>;
  total: number;
  onTransactionClick: (txId: string) => void;
}

const TransactionTable: React.FC<Props> = ({
  transactions,
  page,
  setPage,
  pageSize,
  setPageSize,
  total,
  onTransactionClick,
}) => {
  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setPage(value); // Update the current page
  };

  const handlePageSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPageSize(parseInt(event.target.value, 10)); // Update the page size
  };

  return (
    <div className="mt-6">
      <table className="table-auto w-full border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2">Tx ID</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn, index) => (
            <tr
              key={`${txn.txId}-${index}`}
              className="border-t cursor-pointer hover:bg-gray-200"
              onClick={() => onTransactionClick(txn.txId)}
            >
              <td className="px-4 py-2">{txn.txId}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination Controls */}
      <div className="flex justify-between items-center mt-4">
        <Pagination
          count={Math.ceil(total / pageSize)} // Calculate total number of pages
          page={page} // Current page
          onChange={handlePageChange} // Handle page changes
          color="primary"
        />

        {/* Page Size Control */}
        <div>
          <label className="mr-2">Page Size:</label>
          <input
            type="number"
            value={pageSize}
            onChange={handlePageSizeChange} // Handle page size changes
            className="border px-2 py-1"
            min="1"
            max="100"
          />
        </div>
      </div>
    </div>
  );
};

export default TransactionTable;
