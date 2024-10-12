import React from "react";
import { Transaction } from "../services/api";
import { Pagination } from "@mui/material";

interface Props {
  transactions: Transaction[];
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
  pageSize: number;
  setPageSize: React.Dispatch<React.SetStateAction<number>>;
  total: number;
  onTransactionClick: (txId: string) => void; // New prop for handling row click
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
    setPage(value);
  };

  const handlePageSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPageSize(parseInt(event.target.value, 10));
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
              onClick={() => onTransactionClick(txn.txId)} // Trigger the click event
            >
              <td className="px-4 py-2">{txn.txId}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4">
        <Pagination
          count={Math.ceil(total / pageSize)} // Use total for pagination count
          page={page}
          onChange={handlePageChange}
          color="primary"
        />

        {/* Page Size Control */}
        <div>
          <label className="mr-2">Page Size:</label>
          <input
            type="number"
            value={pageSize}
            onChange={handlePageSizeChange}
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
